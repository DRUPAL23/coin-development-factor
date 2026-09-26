from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse
SEVERITIES={"sev1","sev2","sev3","sev4"}
@dataclass(frozen=True)
class SLOSpec:
    name:str; availability_target:float; latency_p95_ms:int; error_rate_target:float; window_days:int=30; owner:str=""
    def validate(self)->list[str]:
        e=[]
        if not self.name.strip(): e.append("slo.name is required")
        if not 0<self.availability_target<=100: e.append("slo.availability_target must be in (0,100]")
        if self.latency_p95_ms<=0: e.append("slo.latency_p95_ms must be positive")
        if not 0<=self.error_rate_target<100: e.append("slo.error_rate_target must be in [0,100)")
        if self.window_days<=0: e.append("slo.window_days must be positive")
        if not self.owner.strip(): e.append("slo.owner is required")
        return e
@dataclass(frozen=True)
class IncidentPolicy:
    severity:str; acknowledgement_minutes:int; update_interval_minutes:int; escalation_path:tuple[str,...]=(); runbook_url:str=""
    def validate(self)->list[str]:
        e=[]
        if self.severity not in SEVERITIES: e.append(f"unsupported incident severity: {self.severity}")
        if self.acknowledgement_minutes<=0: e.append(f"{self.severity}.acknowledgement_minutes must be positive")
        if self.update_interval_minutes<=0: e.append(f"{self.severity}.update_interval_minutes must be positive")
        if not self.escalation_path: e.append(f"{self.severity}.escalation_path is required")
        if urlparse(self.runbook_url).scheme not in {"http","https"}: e.append(f"{self.severity}.runbook_url must use http(s)")
        return e
@dataclass(frozen=True)
class OperationsSpec:
    name:str; service:str; environment:str; slos:tuple[SLOSpec,...]=(); incident_policies:tuple[IncidentPolicy,...]=(); paging_enabled:bool=False; metrics_enabled:bool=False; logs_enabled:bool=False; traces_enabled:bool=False; oncall_roster:tuple[str,...]=(); status_page_url:str=""; metadata:dict[str,Any]=field(default_factory=dict)
    def validate(self)->list[str]:
        e=[]
        if not self.name.strip(): e.append("operations.name is required")
        if not self.service.strip(): e.append("operations.service is required")
        if self.environment not in {"testnet","staging","mainnet"}: e.append("operations.environment is unsupported")
        if not self.slos: e.append("operations.slos must not be empty")
        if not self.incident_policies: e.append("operations.incident_policies must not be empty")
        if not self.paging_enabled: e.append("operations.paging_enabled must be true")
        if not self.metrics_enabled: e.append("operations.metrics_enabled must be true")
        if not self.logs_enabled: e.append("operations.logs_enabled must be true")
        if not self.traces_enabled: e.append("operations.traces_enabled must be true")
        if not self.oncall_roster: e.append("operations.oncall_roster must not be empty")
        if urlparse(self.status_page_url).scheme not in {"http","https"}: e.append("operations.status_page_url must use http(s)")
        for s in self.slos: e.extend(s.validate())
        for p in self.incident_policies: e.extend(p.validate())
        if self.environment=="mainnet" and "sev1" not in {p.severity for p in self.incident_policies}: e.append("mainnet requires a sev1 incident policy")
        return e
    def readiness_report(self)->dict[str,Any]:
        errors=self.validate()
        checks={"config_valid":not errors,"observability":self.metrics_enabled and self.logs_enabled and self.traces_enabled,"paging":self.paging_enabled,"oncall":bool(self.oncall_roster),"incident_response":bool(self.incident_policies),"slo_defined":bool(self.slos)}
        return {"ready":not errors,"checks":checks,"validation_errors":errors,"service":self.service,"environment":self.environment}
