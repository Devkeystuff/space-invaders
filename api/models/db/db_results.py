from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DbResults:
    result_id: int = 0
    points: int = 0
    username: str = ""
    created: str = ""
    modified: str = ""
    is_deleted: bool = False
