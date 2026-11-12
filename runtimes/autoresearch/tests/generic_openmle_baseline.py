from __future__ import annotations
import json, os, sys, time, warnings
from pathlib import Path
warnings.filterwarnings('ignore')
os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('MKL_NUM_THREADS','1')
os.environ.setdefault('NUMEXPR_NUM_THREADS','1')
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

def is_prob_column(name: str, sample: pd.Series) -> bool:
    n=name.lower()
    if any(x in n for x in ['prob','score','confidence','chance','risk']): return True
    if pd.api.types.is_float_dtype(sample.dtype):
        vals=pd.to_numeric(sample,errors='coerce').dropna()
        return bool(len(vals) and vals.between(0,1).all())
    return False

def main():
    t0=time.perf_counter(); root=Path.cwd(); data=root/'data'
    train=pd.read_csv(data/'train.csv',low_memory=False)
    test=pd.read_csv(data/'test.csv',low_memory=False)
    sample=pd.read_csv(data/'sample_submission.csv',low_memory=False)
    load_s=time.perf_counter()-t0
    if len(sample)!=len(test): raise RuntimeError(f'sample/test rows differ: {len(sample)}/{len(test)}')
    train_only=[c for c in train.columns if c not in test.columns]
    if len(train_only)!=1:
        candidates=[c for c in sample.columns if c in train.columns and c not in test.columns]
        if len(candidates)==1: train_only=candidates
    if len(train_only)!=1: raise RuntimeError(f'cannot infer one target: train_only={train_only}')
    target=train_only[0]
    common=[c for c in train.columns if c in test.columns]
    if not common: raise RuntimeError('no shared features')
    y=train[target]
    keep=y.notna(); y=y[keep]; X=train.loc[keep,common].copy(); Xt=test[common].copy()
    
    for d in (X,Xt):
        for c in d.columns:
            if pd.api.types.is_numeric_dtype(d[c]): d[c]=pd.to_numeric(d[c],errors='coerce').replace([np.inf,-np.inf],np.nan)
            else: d[c]=d[c].astype('string').fillna('__MISSING__').astype(str)
    numeric=[c for c in common if pd.api.types.is_numeric_dtype(X[c]) and pd.api.types.is_numeric_dtype(Xt[c])]
    categorical=[c for c in common if c not in numeric]
    transforms=[]
    if numeric:
        transforms.append(('num',Pipeline([('imp',SimpleImputer(strategy='median')),('scale',StandardScaler(with_mean=False))]),numeric))
    if categorical:
        transforms.append(('cat',Pipeline([('imp',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore',min_frequency=2,max_categories=64))]),categorical))
    prep=ColumnTransformer(transforms,remainder='drop')
    unique=int(y.nunique(dropna=True)); n=max(1,len(y))
    classification=(not pd.api.types.is_numeric_dtype(y)) or (unique<=20 and unique/n<=0.20)
    id_like=[c for c in sample.columns if c.lower() in {'id','row_id','index'} or c.lower().endswith('_id')]
    output_cols=[c for c in sample.columns if c not in test.columns and c not in id_like]
    if not output_cols:
        output_cols=[c for c in sample.columns if c not in id_like]
    if not output_cols: raise RuntimeError(f'cannot infer output columns from {list(sample.columns)}')
    fit0=time.perf_counter()
    if classification:
        le=LabelEncoder(); y_enc=le.fit_transform(y.astype(str)); classes=list(le.classes_)
        model=DummyClassifier(strategy='most_frequent') if len(classes)<2 else LogisticRegression(max_iter=200,solver='lbfgs',n_jobs=1)
        pipe=Pipeline([('prep',prep),('model',model)]); pipe.fit(X,y_enc)
    else:
        y_num=pd.to_numeric(y,errors='coerce'); good=y_num.notna(); X=X.loc[good]; y_num=y_num.loc[good]
        model=DummyRegressor(strategy='mean') if y_num.nunique()<2 else Ridge(alpha=1.0)
        pipe=Pipeline([('prep',prep),('model',model)]); pipe.fit(X,y_num)
    fit_s=time.perf_counter()-fit0
    pred0=time.perf_counter(); out=sample.copy()
    if classification:
        pred_idx=np.asarray(pipe.predict(Xt),dtype=int); pred_labels=le.inverse_transform(np.clip(pred_idx,0,len(le.classes_)-1))
        probs=None
        if hasattr(pipe,'predict_proba') and len(le.classes_)>=2:
            try: probs=np.asarray(pipe.predict_proba(Xt))
            except Exception: probs=None
        if len(output_cols)==1:
            c=output_cols[0]
            if len(le.classes_)==2 and probs is not None and is_prob_column(c,sample[c]): out[c]=probs[:,1]
            else:
                
                numeric_labels=pd.to_numeric(pd.Series(pred_labels),errors='coerce')
                out[c]=numeric_labels.to_numpy() if numeric_labels.notna().all() else pred_labels
        elif probs is not None and len(output_cols)==probs.shape[1]:
            for j,c in enumerate(output_cols):out[c]=probs[:,j]
        else:
            for c in output_cols:out[c]=pred_labels
    else:
        p=np.asarray(pipe.predict(Xt),dtype=float)
        for c in output_cols:
            sample_num=pd.to_numeric(sample[c],errors='coerce').dropna()
            q=p.copy()
            if len(sample_num) and float(sample_num.min())>=0: q=np.maximum(q,0)
            if len(sample_num) and float(sample_num.min())>=0 and float(sample_num.max())<=1 and any(x in c.lower() for x in ['prob','rate','share','ratio','percent','chance','risk']): q=np.clip(q,0,1)
            out[c]=q
    pred_s=time.perf_counter()-pred0
    write0=time.perf_counter(); out.to_csv(root/'submission.csv',index=False); write_s=time.perf_counter()-write0
    total=time.perf_counter()-t0
    print(json.dumps({'status':'ok','train_rows':len(train),'test_rows':len(test),'features':len(common),'target':target,'output_cols':output_cols,'classification':classification,'target_unique':unique,'load_s':load_s,'fit_s':fit_s,'predict_s':pred_s,'write_s':write_s,'total_s':total},sort_keys=True))
if __name__=='__main__':
    try: main()
    except Exception as e:
        print(json.dumps({'status':'error','error_type':type(e).__name__,'error':str(e)},sort_keys=True))
        raise
