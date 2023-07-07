from pydantic import BaseModel


class LoginDataModel(BaseModel):
    username: str
    hashed_pwd: str
