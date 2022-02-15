from dataclasses import dataclass, field
from typing import List
from dataclasses_json import dataclass_json
from pydantic import BaseModel

from models.db.db_result import DbResult


@dataclass_json
@dataclass
class ResponseGetAllResults:
    # results: List[DbResult] = field(default_factory=List)
    is_success: bool = False
    error_code: int = 0
    error_message: str = ""
