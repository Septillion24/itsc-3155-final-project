from datetime import datetime

class User:
    user_id  = None
    username  = None
    email  = None
    first_name  = None
    last_name  = None

    def __init__(self, user_id: str, username: str, email: str, first_name: str, last_name: str, ) -> None:
        self.user_id = user_id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            
        }
    
class FriendRelationship:
    id: int = None
    user1: int = None
    user2: int = None

    def __init__(self, id: int, user1: int, user2: int) -> None:
        self.id = id
        self.user1 = user1
        self.user2 = user2

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user1': self.user1,
            'user2': self.user2
        }
        


class Image:
    image_id: int = None
    url: str = None
    author: int = None

    def __init__(self, image_id: int, url: str, author: int) -> None:
        self.image_id = image_id
        self.url = url
        self.author = author

    def to_dict(self) -> dict:
        return {
            'image_id': self.image_id,
            'url': self.url,
            'author': self.author
        }
from datetime import datetime

class Post:
    post_id: int = None
    owner: User = None
    title: str = None
    image: Image = None
    text_content: str = None
    timestamp: datetime = None
    number_of_comments: int = None

    def __init__(self, post_id: int, owner: User, title: str, image: Image, text_content: str, timestamp: datetime) -> None:
        self.post_id = post_id
        self.owner = owner
        self.title = title
        self.image= image
        self.text_content = text_content
        self.timestamp = timestamp
        self.number_of_comments = (post_id)

    def to_dict(self) -> dict:
        return {
            'post_id': self.post_id,
            'owner': self.owner,
            'title': self.title,
            'image': self.image,
            'text_content': self.text_content,
            'timestamp': str(self.timestamp)
        }
    def updateNumberOfComments(self, db): 
        self.number_of_comments = db.numberOfComments(self.post_id)

class Comment:
    comment_id: int = None
    owner: int = None
    post_id: int = None
    content: str = None
    timestamp: datetime = None

    def __init__(self, comment_id: int, owner: int, post_id: int, content: str, timestamp: datetime) -> None:
        self.comment_id = comment_id
        self.owner = owner
        self.post_id = post_id
        self.content = content
        self.timestamp = timestamp

    def to_dict(self) -> dict:
        return {
            'comment_id': self.comment_id,
            'owner': self.owner,
            'post_id': self.post_id,
            'content': self.content,
            'timestamp': self.timestamp
        }
    
class Vote:
    vote_id: int = None
    owner: User = None
    poll_id: int = None
    vote_for: bool = None
    timestamp: datetime = None

    def __init__(self, vote_id: int, owner: User, poll_id: int, vote_for: bool, timestamp: datetime) -> None:
        self.vote_id = vote_id
        self.owner = owner
        self.poll_id = poll_id
        self.vote_for = vote_for
        self.timestamp = timestamp

    def to_dict(self) -> dict:
        return {
            'vote_id': self.vote_id,
            'owner': self.owner,
            'poll_id': self.poll_id,
            'vote_for': self.vote_for,
            'timestamp': self.timestamp
        }