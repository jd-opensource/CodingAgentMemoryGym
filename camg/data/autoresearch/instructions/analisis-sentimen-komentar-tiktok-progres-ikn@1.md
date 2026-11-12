# OpenMLE-fast task

Task ID: `analisis-sentimen-komentar-tiktok-progres-ikn@1`

Native metric: `TikTokSentimentMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2465 bytes)
- `data/sample_submission.csv` (5007 bytes); columns: ["id", "label"]
- `data/test.csv` (17282 bytes); columns: ["id", "text"]
- `data/train.csv` (80938 bytes); columns: ["id", "text", "label"]

## Public description

Competition: Sentimen Komentar TikTok tentang Progres IKN (Bahasa Indonesia)

Problem statement
Peserta diminta membangun model pembelajaran mesin untuk mengklasifikasikan sentimen komentar TikTok berbahasa Indonesia tentang progres IKN sebagai “positif” atau “negatif”. Komentar bersifat informal (slang, singkatan, campur kode), pendek, dan noisy—sehingga menantang untuk diekstraksi sinyal semantiknya.

Data description
- Satuan data: Setiap baris adalah satu komentar teks.
- Fitur: text (isi komentar).
- Target: label (nilai valid: “positif”, “negatif”).
- Ukuran: 1.472 komentar berlabel.
- Pembagian: Dataset dibagi menjadi train (berlabel) dan test (tanpa label) secara stratified. Teks yang identik dikelompokkan agar tidak tersebar lintas split untuk mencegah kebocoran label.

Disediakan untuk peserta
- train.csv — Kolom: id, text, label
- test.csv — Kolom: id, text
- sample_submission.csv — Kolom: id, label (contoh format). Gunakan hanya label valid: “positif”, “negatif”.

Submission format
- File submission: CSV dengan kolom persis: id,label
- id pada submission harus cocok satu-per-satu dengan id pada test.csv (tanpa baris ganda/hilang/ekstra).
- label harus berupa salah satu dari: “positif”, “negatif” (case-sensitive).

Evaluation
- Metrik: Macro F1 antara prediksi dan label kebenaran pada dua kelas {“positif”, “negatif”}.
- Definisi: Rata-rata F1 dari kedua kelas, dengan penanganan zero-division sebagai 0.0. Metrik ini adil terhadap ketidakseimbangan kelas (sekitar 53% vs 47%) dan menilai performa pada kedua kelas secara seimbang.

Catatan penting
- Tidak ada informasi tambahan di luar teks komentar. Jangan gunakan path atau metadata file sebagai fitur.
- Teks telah melalui pembersihan dasar (case folding, penghapusan URL/mention/tanda baca tertentu), namun normalisasi slang/variasi ejaan masih menjadi tantangan. Teknik yang disarankan: tokenisasi subword, representasi karakter, normalisasi leksikal, model pralatih bahasa Indonesia/multibahasa (mis. IndoBERT, mBERT, XLM-R), atau pendekatan klasik (n-gram + model linear).
- Tidak ada batasan ukuran/kompleksitas model; efisiensi komputasi menjadi tanggung jawab peserta.

Tujuan kompetisi
- Merancang pipeline end-to-end: pemrosesan data, rekayasa fitur, pelatihan model, dan evaluasi.
- Mendorong strategi robust terhadap teks pendek, noisy, dan campur kode, dengan fokus pada generalisasi di domain media sosial Indonesia.
