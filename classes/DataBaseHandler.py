from classes.User import User
import psycopg

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
        with psycopg.connect(
        conninfo = "dbname=postgres user=postgres password=changeme host=localhost"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM posts')
                rows = cur.fetchall()
                return
            
    def createPost(self, user:User, title:str, content:str):
        pass

    def getPostByID(self, postID: int):
        with psycopg.connect(
        conninfo = "dbname=postgres user=postgres password=changeme host=localhost"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT * FROM posts WHERE posts.postID = {postID}')
                rows = cur.fetchall()
                return rows
    def getUsers(self):
        with psycopg.connect(
        conninfo = "dbname=postgres user=postgres password=changeme host=localhost"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM users')
                rows = cur.fetchall()
                return rows

    def createUser(self):
        pass

    def getUserByID(self, userID: str):
        with psycopg.connect(
        conninfo = "dbname=postgres user=postgres password=changeme host=localhost"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f'select * from users where users.username = \'{userID}\'')
                rows = cur.fetchall()
                print(rows)
        
    