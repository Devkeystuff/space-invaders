from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ResponseSaveResult:
    result_id: int = 0
    is_success: bool = False
    error_code: int = 0
    error_message: str = ""
