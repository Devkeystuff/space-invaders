from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RequestSaveResult:
    points: int = 0
    username: str = ""
