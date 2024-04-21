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
                cur.execute(f'SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM posts WHERE posts.postID = {postID}')
                rows = cur.fetchall()
                selectedPost = Post(rows[0].keys[0], rows[0].keys[1], rows[0].keys[2], rows[0].keys[3], rows[0].keys[4], rows[0].keys[5])
                return selectedPost
            
            #sneed to update VVV
    def getUsers(self):
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM users')
                rows = cur.fetchall()
                return rows
            #sneed to make VVV
    def createUser(self):
        pass
            #sneed to update VVV
    def getUserByID(self, userID: str):
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f'select * from users where users.username = \'{userID}\'')
                rows = cur.fetchall()
                print(rows)
        
    