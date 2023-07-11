from pydantic import BaseModel


class C2SPostModel(BaseModel):
    title: str | None = None
    content: str
    parent: int | None = None
