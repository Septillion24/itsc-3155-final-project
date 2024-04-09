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