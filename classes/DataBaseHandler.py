from classes.User import User


class DataBaseHandler:
    instance = None
    # TODO: @James, fill this out
    def __init__(self):
        pass    
        
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
    
    # these methods are not final, change them if you will
    def getPosts(self):
        pass
    def createPost(self, user:User, title:str, content:str):
        pass
    def getUsers(self):
        pass
    def createUser(self):
        pass
        
    