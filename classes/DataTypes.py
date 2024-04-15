class User:
    userName = None
    userID = None
    
    def __init__(self, userName:str, userID:int):
        self.userName = userName
        self.userID = userID 
        
    def to_dict(self):
        return {
            "userName" : self.userName,
            "userID": self.userId,
        }
        
class Post:
    title = None
    content = None
    parentUserID = None
    
    def __init__(self, title:str, content:str, parentUserID:int):
        self.title = title
        self.content = content
        self.parentUserID = parentUserID
        
    def to_dict(self):
        return {
            "title" : self.title,
            "content": self.content,
            "parentUserID": self.parentUserID
        }
        
class Comment:
    commentID = None
    content = None
    parentUserID = None
    parentPostID = None
    
    def __init__(self, commentID:int, content:str, parentUserID:int, parentPostID:int):
        self.commentID = commentID
        self.content = content
        self.parentUserID = parentUserID
        self.parentPostID = parentPostID
        
    def to_dict(self):
        return {
            "commentID" : self.commentID,
            "content": self.content,
            "parentUserID": self.parentUserID,
            "parentPostID": self.parentPostID
        }