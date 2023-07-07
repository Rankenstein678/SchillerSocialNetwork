from pydantic import BaseModel


class LoginDataModel(BaseModel):
    userEmail: str
    hashed_pwd: str
