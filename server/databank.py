import mariadb
from dotenv import dotenv_values

from models.SentPostModel import SentPostModel

SQL_SERVER_ADDRESS = "192.168.3.232"

secrets = dotenv_values("secrets.env")


def connect_to_db():
    conn = mariadb.connect(host=SQL_SERVER_ADDRESS, user=secrets.get('SQL_USER'),
                           password=secrets.get('SQL_PASSWORD'),
                           database="octopost_production", port=3306)
    cursor = conn.cursor()

    return cursor, conn


def get_newest_posts(amount: int):
    cursor = connect_to_db()[0]
    cursor.execute("SELECT * FROM posts ORDER BY postID DESC LIMIT %s", (amount,))
    data = cursor.fetchall()
    cursor.close()
    return data


def get_post_by_id(post_id: int):
    cursor = connect_to_db()[0]
    cursor.execute("SELECT * FROM posts WHERE postID = %s", (post_id,))
    data = cursor.fetchall()
    cursor.close()
    return data


def put_post(post: SentPostModel, user_id):
    cursor, connection = connect_to_db()
    cursor.execute("INSERT INTO posts (userID, title, content, likes, parentPost) VALUES (%s, %s, %s, %s, %s)",
                   (user_id, post.title, post.content, 0, post.parent))
    connection.commit()
    cursor.close()


def like_post(post_id: int, user_id: int):
    pass
