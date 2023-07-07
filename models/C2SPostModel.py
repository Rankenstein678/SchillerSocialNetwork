from pydantic import BaseModel


class C2SPostModel(BaseModel):
    title: str
    content: str
    parent: int | None = None
