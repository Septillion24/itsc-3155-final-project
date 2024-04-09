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