from typing import Optional
from pydantic import BaseModel, validator


class Secret(BaseModel):
    secret_text: str
    phrase: str
    secret_key: Optional[str]

    @validator('secret_text')
    def secret_text_must_exist(cls, v):
        if not v:
            raise ValueError("Field 'secret_text' can not be empty")
        return v

    @validator('phrase')
    def phrase_must_exist(cls, v):
        if not v:
            raise ValueError("Field 'phrase' can not be empty")
        return v
