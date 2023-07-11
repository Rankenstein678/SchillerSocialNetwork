from pydantic import BaseModel


class S2CPostModel(BaseModel):
    postID: int
    creatorEmail: str
    title: str | None = None
    content: str
    likes: int
    parent: int | None = None
