from pydantic import BaseModel


class S2CPostModel(BaseModel):
    creatorEmail: str
    title: str
    content: str
    likes: int
    parent: int | None = None
