from classes.User import User


class DataBaseHandler:
    instance = None
    # TODO: @James, fill this out
    def __init__(self):
        pass    
        
    @classmethod
    def getInstance(cls):
        if cls.instance != None:
            cls.instance = cls()
        return cls.instance
    
    # these methods are not final, change them if you will
    def getPosts():
        pass
    def createPost(user:User, title:str, content:str):
        pass
    def getUsers():
        pass
    def createUser():
        pass
        
    