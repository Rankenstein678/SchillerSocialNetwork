from fastapi import FastAPI

import server.databank
from models.LoginDataModel import LoginDataModel
from models.SentPostModel import SentPostModel

app = FastAPI()


@app.get("/posts")
def get_new_posts(amount: int | None = None):
    if amount is None:
        amount = 10
    return server.databank.get_newest_posts(amount)


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int):
    return server.databank.get_post_by_id(post_id)


@app.post("/posts")
def make_post(post: SentPostModel, user_id: int):  # Todo: Implement login functionality
    return server.databank.put_post(post, user_id)


@app.patch("/posts/{post_id}")
def update_like(post_id: int, user_id: int):  # Todo: Implement login functionality
    return server.databank.update_like_status(post_id, user_id)


@app.get("/salts/{username}")
def get_salt(username: str):
    return {"salt": "PLACEHOLDER"}


@app.post("/login")
def login_user(login_data: LoginDataModel):
    return login_data
