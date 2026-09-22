from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
from .models import AuditFinding, LaunchControlSpec

def load_spec(path: str | Path) -> LaunchControlSpec:
    raw: dict[str, Any] = yaml.safe_load(Path(path).read_text()) or {}
    raw = raw.get('audit', raw)
    findings = tuple(AuditFinding(**{k:v for k,v in item.items() if k in {'finding_id','severity','title','status','owner','evidence','remediation'}}) for item in raw.get('findings', []) or [])
    return LaunchControlSpec(name=str(raw.get('name','')), release_version=str(raw.get('release_version','')), network=str(raw.get('network','testnet')), controls={str(k):bool(v) for k,v in (raw.get('controls') or {}).items()}, findings=findings, evidence={str(k):str(v) for k,v in (raw.get('evidence') or {}).items()}, change_freeze=bool(raw.get('change_freeze',False)), rollback_window_minutes=int(raw.get('rollback_window_minutes',0)), signoff_roles=tuple(str(x) for x in raw.get('signoff_roles',[]) or []), metadata=raw.get('metadata') or {})

def summary(spec: LaunchControlSpec) -> dict[str, object]:
    return spec.report()
