class Post():
    def __init__(self, postID, userID, text, likes, inputcase):
        self.inputcase = inputcase
        self.postID = postID
        self.userID = userID
        self.text = text
        self.likes = likes

    def __str__(self):
        return "Post:{" + str(self.postID) + ", " + str(self.userID) + ", " + self.text + ", " + str(self.likes) + "}"


class ClientPost():
    def __init__(self, userName, password, text):
        self.userName = userName
        self.password = password  # incredible Security - protected by SchillerSpirit
        self.text = text
