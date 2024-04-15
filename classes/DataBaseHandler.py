from classes.DataTypes import User, Post, Comment
import psycopg
from db_secrets import db_info

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
    
    
    def getPosts(self):
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM post')
                rows = cur.fetchall()
                return rows
            
    def createPost(self, user:User, content:str, commentIDs:list):
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                # double check commentIDs value passing
                cur.execute(F'''INSERT INTO posts (username, content, commentIDs) VALUES
                    ('{user.name}', '{content}', '{commentIDs}')''')
                

    def getPostByID(self, postID: int):
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM posts WHERE posts.postID = {postID}')
                rows = cur.fetchall()
                return rows
    def getUsers(self):
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM users')
                rows = cur.fetchall()
                return rows

    def createUser(self):
        pass

    def getUserByID(self, userID: str):
        with psycopg.connect(
        conninfo = db_info()
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f'select * from users where users.username = \'{userID}\'')
                rows = cur.fetchall()
                print(rows)
        
    