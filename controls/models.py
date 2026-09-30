from dataclasses import dataclass
@dataclass(frozen=True)
class ControlSpec:
    name: str
    enabled: bool = True
