import mariadb
from dotenv import dotenv_values
from models import C2SPostModel
from models.S2CPostModel import S2CPostModel

SQL_SERVER_ADDRESS = "192.168.3.232"

secrets = dotenv_values("secrets.env")


def connect_to_db():
    conn = mariadb.connect(host=SQL_SERVER_ADDRESS, user=secrets.get('SQL_USER'),
                           password=secrets.get('SQL_PASSWORD'),
                           database="octopost_production", port=3306)
    cursor = conn.cursor()

    return cursor, conn

def get_newest_posts(amount: int, after: int | None):
    cursor = connect_to_db()[0]
    if after is None:
        cursor.execute("SELECT * FROM posts ORDER BY postID DESC LIMIT %s", (amount,))
    else:
        cursor.execute("SELECT * FROM posts WHERE postID < %s ORDER BY postID DESC LIMIT %s", (after, amount,))
    data = cursor.fetchall()
    cursor.close()
    return list(map(lambda post:
                    S2CPostModel(postID=post[0], username=post[1], title=post[2], content=post[3], likes=post[4],
                                 parent=post[5]), data))


def get_post_by_id(post_id: int):
    cursor = connect_to_db()[0]
    cursor.execute("SELECT * FROM posts WHERE postID = %s", (post_id,))
    data = cursor.fetchall()[0]
    cursor.close()
    return S2CPostModel(postID=data[0], username=data[1], title=data[2], content=data[3], likes=data[4],
                        parent=data[5])


def put_post(post: C2SPostModel, username: str):
    cursor, connection = connect_to_db()
    # Don't allow titles on comments
    if post.parent is not None:
        post.title = None
    cursor.execute("INSERT INTO posts (username, title, content, likes, parentPost) VALUES (%s, %s, %s, %s, %s)",
                   (username, post.title, post.content, 0, post.parent))
    connection.commit()
    cursor.close()


def update_like_status(post_id: int, username: str):
    cursor, connection = connect_to_db()
    cursor.execute("SELECT * FROM liked_by WHERE postID = %s AND username = %s",
                   (post_id, username))
    already_liked = cursor.fetchone()
    if already_liked is None:
        cursor.execute("INSERT INTO liked_by (postID, username) VALUES (%s, %s)",
                       (post_id, username))
        cursor.execute("UPDATE posts SET likes = likes + 1 WHERE postID = %s",
                       (post_id,))
    else:
        cursor.execute("DELETE FROM liked_by WHERE postID = %s AND username = %s",
                       (post_id, username))
        cursor.execute("UPDATE posts SET likes = likes - 1 WHERE postID = %s",
                       (post_id,))
    connection.commit()
    cursor.close()

def create_user(username: str, hash: int):
    cursor, connection = connect_to_db()
    cursor.execute("INSERT INTO users(username, password) VALUES {%s, %s}", (username, hash))
    connection.commit()
    cursor.close()
    return(f'Der User {username} wurde erfolgreich erstellt.')