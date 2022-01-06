from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class RequestUserRegister:
    api_key: str = ""
    user_id: int = 0
    email: str = ""