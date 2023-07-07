from pydantic import BaseModel


class S2CPostModel(BaseModel):
    creatorID: int
    title: str
    content: str
    likes: int
    parent: int | None = None
