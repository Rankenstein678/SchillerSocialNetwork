# each post is represented by an object
class Post():
    def __init__(self, postID, userID, title, text, likes, inputcase):
        self.title = title
        self.inputcase = inputcase
        self.postID = postID
        self.userID = userID
        self.text = text
        self.likes = likes

    def __str__(self):
        return "Post:{" + str(self.postID) + ", " + str(self.userID) + ", " + self.title + ", " + self.text + ", " + str(self.likes) + "}"


class ClientPost():
    def __init__(self, userName, password, title, text, inputcase):
        self.title = title
        self.inputcase = inputcase
        self.userName = userName
        self.password = password
        self.text = text
