from pydantic import BaseModel, validator

from fastapi import HTTPException


class Secret(BaseModel):
    secret_text: str
    phrase: str
    secret_key: str = None

    def validate_fields(self):

        if not self.secret_text:
            raise HTTPException(status_code=400, detail="Field 'secret_text' can not be empty")

        if not self.phrase:
            raise HTTPException(status_code=400, detail="Field 'phrase' can not be empty")
