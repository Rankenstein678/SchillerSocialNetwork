from fastapi import FastAPI

from models.LoginDataModel import LoginDataModel
from models.SentPostModel import SentPostModel
from server.databank import get_newest_posts

app = FastAPI()


@app.get("/")
def get_new_posts(amount: int | None = None):
    if amount is None:
        amount = 10
    return get_newest_posts(amount)


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int):
    return {"post_id": post_id}


@app.post("/posts")
def make_post(post: SentPostModel):
    return "not implemented"


@app.patch("/posts/{post_id}")
def like_post(post_id):
    # TODO: PREVENT LIKING OF ONE POSTS
    pass


@app.get("/salts/{username}")
def get_salt(username: str):
    return {"salt": "PLACEHOLDER"}


@app.post("/login")
def login_user(login_data: LoginDataModel):
    return login_data
