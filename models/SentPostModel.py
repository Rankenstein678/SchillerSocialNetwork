from pydantic import BaseModel


class SentPostModel(BaseModel):
    title: str
    content: str
