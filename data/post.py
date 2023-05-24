class Post():
    def __init__(self, postID, userID, text, likes):
        self.postID = postID
        self.userID = userID
        self.text = text
        self.likes = likes

    def __str__(self):
        return "Post:{" + str(self.postID) + ", " + str(self.userID) + ", " + self.text + ", " + str(self.likes) + "}"
