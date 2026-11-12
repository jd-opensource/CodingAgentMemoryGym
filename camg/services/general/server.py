from __future__ import annotations

import logging
import os
from typing import Any, Optional

from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel

from .environment import GeneralEpisodeManager

logging.basicConfig(
    level=os.environ.get("AGENTGENERAL_LOG_LEVEL", "INFO"),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger("camg.services.general.server")

app = FastAPI(title="camg-agentgeneral", version="1.0.0")

_manager: GeneralEpisodeManager | None = None

def get_manager() -> GeneralEpisodeManager:
    if _manager is None:
        raise HTTPException(status_code=503, detail="manager not initialized")
    return _manager

class ResetRequest(BaseModel):
    id: int
    data_idx: int

class StepRequest(BaseModel):
    id: int
    action: str

class CloseRequest(BaseModel):
    id: int

class HorizonRequest(BaseModel):
    id: int

@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/metadata")
def metadata() -> dict[str, Any]:
    return get_manager().metadata()

@app.post("/create")
def create() -> dict[str, Any]:
    slot_id = get_manager().create()
    return {
        "id": slot_id,
        "observation": "",
        "reward": 0.0,
        "done": False,
        "info": {"schema": "agentgeneral_general_v1"},
    }

@app.post("/reset")
def reset(request: ResetRequest) -> dict[str, Any]:
    try:
        return get_manager().reset(request.id, request.data_idx).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except IndexError as exc:
        raise HTTPException(status_code=404, detail=f"data_idx out of range: {exc}") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

@app.post("/step")
def step(request: StepRequest) -> dict[str, Any]:
    try:
        return get_manager().step(request.id, request.action).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

@app.get("/observation")
def observation(id: int = Query(...)) -> str:
    try:
        return get_manager().observation(id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.post("/horizon")
def horizon(request: HorizonRequest) -> dict[str, Any]:
    try:
        return get_manager().finalize_horizon(request.id).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

@app.get("/detail")
def detail(
    id: int = Query(...),
    x_agentgeneral_detail_token: Optional[str] = Header(default=None),
) -> dict[str, Any]:
    expected = os.environ.get("AGENTGENERAL_DETAIL_TOKEN", "")
    if not expected or x_agentgeneral_detail_token != expected:
        raise HTTPException(status_code=403, detail="forbidden")
    try:
        return get_manager().detail(id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.post("/close")
def close(request: CloseRequest) -> dict[str, Any]:
    return get_manager().close(request.id)

def build_manager_from_environment() -> GeneralEpisodeManager:

    parquet_path = os.environ.get("AGENTGENERAL_PARQUET", "")
    if not parquet_path:
        raise RuntimeError("AGENTGENERAL_PARQUET is required")
    mimoagent_config_path = os.environ.get("AGENTGENERAL_MIMOAGENT_CONFIG", "")
    if not mimoagent_config_path:
        raise RuntimeError("AGENTGENERAL_MIMOAGENT_CONFIG is required")
    return GeneralEpisodeManager(
        parquet_path=parquet_path,
        mimoagent_config_path=mimoagent_config_path,
        max_steps=int(os.environ.get("AGENTGENERAL_MAX_STEPS", "200")),
        prompt_policy_turns=(
            int(os.environ["AGENTGENERAL_PROMPT_TURNS"])
            if os.environ.get("AGENTGENERAL_PROMPT_TURNS")
            else None
        ),
        max_observation_bytes=int(
            os.environ.get("AGENTGENERAL_MAX_OBSERVATION_BYTES", str(32768))
        ),
        reward_timeout=float(os.environ.get("AGENTGENERAL_REWARD_TIMEOUT", "1800")),
    )

@app.on_event("startup")
def _startup() -> None:
    global _manager
    if os.environ.get("AGENTGENERAL_LAZY_INIT", "0") != "1":
        _manager = build_manager_from_environment()
        logger.info("manager initialized: %s", _manager.metadata())
        logger.info("boot sweep report: %s", _manager.sweep_claims())
        _manager.start_idle_reaper()


@app.on_event("shutdown")
def close_active_episodes() -> None:
    """Close owned episodes before the foreground service exits."""
    if _manager is not None:
        with _manager._slots_lock:
            slots = list(_manager._slots)
        from camg.services.lifecycle import close_all
        close_all(slots, _manager.close, lambda slot_id: slot_id in _manager._slots)
