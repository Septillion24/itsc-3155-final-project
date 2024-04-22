from classes.DataTypes import User, Post, Comment
import psycopg
from db_secrets import db_info
import datetime

class DataBaseHandler:
    instance = None
    #userID : user instance
    userDict = {}
    #postID : post instance
    postDict = {}
    
    
    # TODO: @James, fill this out
    def __init__(self):
        pass    
        
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
    
    
    def getPosts(self) -> list[Post]: #needs testing 
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM Post')
                rows = cur.fetchall()
                posts = []
                for postrow in rows:
                    posts.add(Post(postrow.keys[0], postrow.keys[1], postrow.keys[2], postrow.keys[3], postrow.keys[4], postrow.keys[5]))
                return posts

                
    def createPost(self, owner: int, title: str, image_id: int, text_content: str, timestamp: datetime): #needs testing 
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(F'''INSERT INTO Post (Owner, Title, ImageID, TextContent, Timestamp) VALUES
                    ('{owner}', '{title}', '{image_id}', '{text_content}', '{timestamp}')''')
                
    def getPostByID(self, postID: int, owner: int, title: str, image_id: int, text_content: str, timestamp: datetime) -> Post: #needs testing
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM Post WHERE Post.postID = {postID}')
                rows = cur.fetchall()
                selectedPost = Post(rows[0].keys[0], rows[0].keys[1], rows[0].keys[2], rows[0].keys[3], rows[0].keys[4], rows[0].keys[5])
                return selectedPost
            
            
    def getUsers(self) -> list[User]: #needs testing
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT UserID, Username, Email, FirstName, LastName, Password FROM User;')
                rows = cur.fetchall()
                users = []
                for userrow in rows:
                    users.add(User(userrow.keys[0], userrow.keys[1], userrow.keys[2], userrow.keys[3], userrow.keys[4], userrow.keys[5]))
                return users
            
    def createUser(self, Username: str, Email: str, FirstName: str, LastName: str, Password: str) -> None: #needs testing
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f'''INSERT INTO User (Username, Email, FirstName, LastName, Password) 
                            VALUES ('{Username}', '{Email}', '{FirstName}', '{LastName}', 
                            '{Password}'); ''')
                
            
    def getUserByID(self, userID: str) -> User:#needs testing
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT UserID, Username, Email, FirstName, LastName, Password FROM User WHERE UserID = \'{userID}\'')
                rows = cur.fetchall()
                userrow = rows[0]
                return User(userrow.keys[0], userrow.keys[1], userrow.keys[2], userrow.keys[3], userrow.keys[4], userrow.keys[5])
        
    def createUserVoteOnPoll(self, userID: int, pollID: int, voteFor: bool) -> None:
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f'''INSERT INTO Vote (Owner, PollID, VoteFor)
                                VALUES ({userID}, {pollID}, {voteFor}); ''')
    def getPostsByUserID(self, userID: int) -> list[Post]:
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT PostID, Owner, Title, ImageID, TextContent FROM Post WHERE Owner = {userID}; ''')
                rows = cur.fetchall()
                posts = []
                for postrow in rows:
                    posts.add(Post(postrow.keys[0], postrow.keys[1], postrow.keys[2], postrow.keys[3], postrow.keys[4]))
                return posts
    def getTopPosts(self, numberOfPosts: int) -> list[Post]:
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT PostID, Owner, Title, ImageID, TextContent FROM Post ORDER BY Timestamp DESC LIMIT {numberOfPosts}; ''')
                rows = cur.fetchall()
                posts = []
                for postrow in rows:
                    posts.add(Post(postrow.keys[0], postrow.keys[1], postrow.keys[2], postrow.keys[3], postrow.keys[4]))
                return posts
            