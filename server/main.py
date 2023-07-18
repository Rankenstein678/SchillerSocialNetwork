from fastapi import FastAPI

import server.databank
from models.LoginDataModel import LoginDataModel
from models.C2SPostModel import C2SPostModel
from models.S2CPostModel import S2CPostModel

app = FastAPI(
    title="Octopost API",
    summary="API für das Octopost Social Network",
    description="Made by: Yannick Bougaran und Phillip Zazzetta - Kontaktiere uns auf Teams!",
    version="0.1.0",
    docs_url="/",
)


@app.get("/posts")
def get_new_posts(amount: int | None = 10, after: int | None = None) -> list[S2CPostModel]:
    """Gibt die ausgewählte Anzahl der neusten Posts zurück.

        **- amount:** Anzahl der auszugebenen Posts, standardmäßig 10
    """
    return server.databank.get_newest_posts(amount, after)


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int) -> S2CPostModel:
    """Gibt den ausgewählten Posts zurück.

        **- post_id:** ID des Posts
    """
    data = server.databank.get_post_by_id(post_id)
    return data


@app.post("/posts")
def make_post(post: C2SPostModel, username: str):  # Todo: Implement login functionality
    """Postet das C2SPostModel

        **- post:** C2SPostModel des zu postenden Inhalts. Parent ist optional
    """
    return server.databank.put_post(post, username)


@app.patch("/posts/{post_id}")
def update_like(post_id: int, username: str):  # Todo: Implement login functionality
    """Liked / Entliked den Post

        **- post_id:** ID des Posts
    """
    return server.databank.update_like_status(post_id, username)


@app.get("/salts/{username}")
def get_salt(username: str):
    return {"salt": "PLACEHOLDER"}


@app.post("/login")
def login_user(login_data: LoginDataModel):
    return login_data

@app.post("/createu")
def create_user(username: str, hash: int):
    return server.databank.create_user(username, hash)