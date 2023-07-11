from pydantic import BaseModel


class LoginDataModel(BaseModel):
    username: str
    hash: str
