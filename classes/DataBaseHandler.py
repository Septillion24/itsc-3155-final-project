from classes.DataTypes import User, Post, Comment, Image, Vote
import psycopg
from dotenv import load_dotenv
import datetime
import os
from psycopg_pool import ConnectionPool


load_dotenv()

pool = None


def get_pool():
    global pool
    if pool is None:
        pool = ConnectionPool(
            conninfo=os.getenv('DB_CONNECTION_STRING', ''),
        )
    return pool
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
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM Post')
                rows = cur.fetchall()
                posts = []
                for postrow in rows:
                    posts.append(Post(postrow[0], postrow[1], postrow[2], postrow[3], postrow[4], postrow[5]))
                return posts

                
    def createPost(self, owner: str, title: str, image: Image, text_content: str, timestamp: datetime) ->   Post: 
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(F'''INSERT INTO Post (Owner, Title, ImageID, TextContent, Timestamp) VALUES
                    ('{owner}', '{title}', '{image.image_id}', '{text_content}', '{timestamp}')''')
                return self.getMostRecentPost()
        
                
    def getPostByID(self, postID: int) -> Post: #needs testing
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM Post WHERE Post.postID = {postID}')
                rows = cur.fetchall()
                selectedPost = Post(rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4], rows[0][5])
                return selectedPost
            
            
    def getUsers(self) -> list[User]: #needs testing
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT UserID, Username, Email, FirstName, LastName FROM Users;')
                rows = cur.fetchall()
                users = []
                for userrow in rows:
                    users.append(User(userrow[0], userrow[1], userrow[2], userrow[3], userrow[4]))
                return users
            
    def createUser(self, userID: str, username: str, email: str, firstname: str, lastname: str) -> User: 
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''INSERT INTO Users (UserID, Username, Email, FirstName, LastName) 
                            VALUES ('{userID}', '{username}', '{email}', '{firstname}', '{lastname}' 
                            ); ''')
                return User(userID, username, email, firstname, lastname)
                
            
    def getUserByID(self, userID: str) -> User:#needs testing
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT UserID, Username, Email, FirstName, LastName FROM Users WHERE UserID = \'{userID}\'')
                if cur.rowcount == 0:
                    return None
                rows = cur.fetchall()
                userrow = rows[0]
                return User(userrow[0], userrow[1], userrow[2], userrow[3], userrow[4])
        
    def createUserVoteOnPoll(self, userID: int, pollID: int, voteFor: bool) -> Vote: 
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''INSERT INTO Vote (Owner, PollID, VoteFor)
                                VALUES ({userID}, {pollID}, {voteFor}); ''')
                return self.getMostRecentVote()
    def getMostRecentVote(self) -> Vote: 
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT VoteID, Owner, PollID, VoteFor FROM Vote ORDER BY VoteID DESC LIMIT 1')
                rows = cur.fetchall()
                mostRecentVote = Vote(rows[0][0], self.getUserByID(rows[0][1]), rows[0][2], rows[0][3])
                return mostRecentVote
    def getPostsByUserID(self, userID: int) -> list[Post]:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
<<<<<<< Updated upstream
                cur.execute(f'''SELECT PostID, Owner, Title, ImageID, TextContent FROM Post WHERE Owner = {userID}; ''')
=======
                cur.execute(f'''SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM Post WHERE Owner = '{userID}'; ''')
>>>>>>> Stashed changes
                rows = cur.fetchall()
                posts = []
                for postrow in rows:
                    posts.append(Post(postrow[0], postrow[1], postrow[2], postrow[3], postrow[4], postrow[5], self.numberOfComments(postrow[0])))
                return posts
    def getMostRecentPost(self) -> Post: #needs testing
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM Post ORDER BY PostID DESC LIMIT 1')
                rows = cur.fetchall()
                mostRecentPost = Post(rows[0][0], self.getUserByID(rows[0][1]), rows[0][2], rows[0][3], rows[0][4], rows[0][5])
                return mostRecentPost
            
    def getTopPosts(self, numberOfPosts: int) -> list[Post]:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM Post ORDER BY Timestamp DESC LIMIT {numberOfPosts}; ''')
                rows = cur.fetchall()
                posts = []
                for postrow in rows:
                    posts.append(Post(postrow[0], postrow[1], postrow[2], postrow[3], postrow[4], postrow[5]))
                return posts
    def numberOfComments(self, postID: int) -> int:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT COUNT(*) FROM Comment WHERE PostID = '{postID}'; ''')
                rows = cur.fetchall()
                return rows[0]
            
    def getImageByID(self, imageID: int) -> str:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT ImageID, URL, Author FROM Image WHERE ImageID = {imageID}; ''')
                rows = cur.fetchall()
                return Image(rows[0][0], rows[0][1], rows[0][2])
    
    def createFriendRelationship(self, user1: int, user2: int) -> None:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''INSERT INTO Friends (User1, User2) VALUES ({user1}, {user2}); ''')
    
    def getFriends(self, userID: int) -> list[User]:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT User1, User2 FROM Friends WHERE User1 = {userID} OR User2 = {userID}; ''')
                rows = cur.fetchall()
                friends = []
                for friendrow in rows:
                    friends.append(User(friendrow[0], friendrow[1]))
                return friends
    def createImage(self, url: str, author: int) -> None: 
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''INSERT INTO Image (URL, Author) VALUES ('{url}', {author}); ''')
            return self.getMostRecentImage()
    def getMostRecentImage(self) -> Image:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT ImageID, URL, Author FROM Image ORDER BY ImageID DESC LIMIT 1')
                rows = cur.fetchall()
                mostRecentImage = Image(rows[0][0], rows[0][1], rows[0][2])
                return mostRecentImage
    def createComment(self, post: Post, owner: User, text: str, timestamp: datetime) -> None: 
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''INSERT INTO Comment (PostID, Owner, Text, Timestamp) VALUES ({post.post_id}, {owner.user_id}, '{text}', '{timestamp}'); ''')
            return self.getMostRecentComment()
    def getMostRecentComment(self) -> Comment: 
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT CommentID, PostID, Owner, Text, Timestamp FROM Comment ORDER BY CommentID DESC LIMIT 1')
                rows = cur.fetchall()
                mostRecentComment = Comment(rows[0][0], self.getPostByID(rows[0][1]), self.getUserByID(rows[0][2]), rows[0][3], rows[0][4])
                return mostRecentComment
    def getCommentsByPostID(self, postID: int) -> list[Comment]:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT CommentID, PostID, Owner, Text, Timestamp FROM Comment WHERE PostID = {postID}; ''')
                rows = cur.fetchall()
                comments = []
                for commentrow in rows:
                    comments.append(Comment(commentrow[0], commentrow[1], commentrow[2], commentrow[3], commentrow[4]))
                return comments
    def getCommentsByUserID(self, userID: int) -> list[Comment]:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT CommentID, PostID, Owner, Text, Timestamp FROM Comment WHERE Owner = {userID}; ''')
                rows = cur.fetchall()
                comments = []
                for commentrow in rows:
                    comments.append(Comment(commentrow[0], commentrow[1], commentrow[2], commentrow[3], commentrow[4]))
                return comments