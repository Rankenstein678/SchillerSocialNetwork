import mariadb
from dotenv import dotenv_values

from models.SentPostModel import SentPostModel

SQL_SERVER_ADDRESS = "192.168.3.232"

secrets = dotenv_values("secrets.env")


# TODO:Secrets!!
def connect_to_db():
    conn = mariadb.connect(host=SQL_SERVER_ADDRESS, user=secrets.get('SQL_USER'),
                               password=secrets.get('SQL_PASSWORD'),
                               database="octopost_production", port=3306)
    cursor = conn.cursor()

    return cursor


def get_newest_posts(amount: int):
    cursor = connect_to_db()
    cursor.execute("SELECT * FROM posts ORDER BY postID DESC LIMIT 10")
    data = cursor.fetchall()
    cursor.close()
    return data


def get_post_by_id(post_id: int):
    cursor = connect_to_db()
    cursor.execute("SELECT * FROM posts p WHERE p.postID = %s", (post_id,))
    data = cursor.fetchall()
    cursor.close()


def put_post(post: SentPostModel):
    user_id = -1  # TODO: IMPLEMENT USER
    cursor = connect_to_db()
    cursor.execute("INSERT INTO posts (userID, title, text, likes) VALUES (%s, %s, %s, %s)",
                   (user_id, post.title, post.content, 0))
    cursor.close()


def like_post(post_id: int):
    pass
    # TODO: Missing Databank structure needed
