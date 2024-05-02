from classes.DataTypes import User, Post, Comment, Image, Vote
import psycopg
from dotenv import load_dotenv
import datetime 
import os
from psycopg_pool import ConnectionPool
import time


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
                    ('{owner}', '{title}', '{image.image_id}', '{text_content}', '{timestamp}') RETURNING PostID; ''')
                rows = cur.fetchall()
                return Post(rows[0][0], owner, title, image, text_content, timestamp)
            
        
                
    def getPostByID(self, postID: int) -> Post: #needs testing
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM Post WHERE Post.postID = {postID}')
                rows = cur.fetchall()
                selectedPost = Post(rows[0][0], rows[0][1], rows[0][2], self.getImageByID(rows[0][3]), rows[0][4], rows[0][5])
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
        
    
    def getPostsByUserID(self, userID: int) -> list[Post]:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM Post WHERE Owner = '{userID}'; ''')
                rows = cur.fetchall()
                posts = []
                for postrow in rows:
                    posts.append(Post(postrow[0], postrow[1], postrow[2], postrow[3], postrow[4], postrow[5]))
                return posts
            
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
                cur.execute(f'''SELECT COUNT(*) FROM Comment WHERE PostID = {postID}; ''')
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
                cur.execute(f'''INSERT INTO Image (URL, Author) VALUES ('{url}', {author}) RETURNING ImageID; ''')
                rows = cur.fetchall()
                return Image(int(rows[0][0]), url, author)
    def createComment(self, post: Post, owner: User, content: str, timestamp: datetime) -> None: 
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''INSERT INTO Comment (PostID, Owner, Content, Timestamp) VALUES ({post.post_id}, {owner.user_id}, '{content}', '{timestamp}') RETURNING CommentID; ''')
                rows = cur.fetchall()
                return Comment(int(rows[0][0]), owner, post.post_id, content, timestamp)
    def getCommentsByPostID(self, postID: int) -> list[Comment]:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT CommentID, PostID, Owner, Content, Timestamp FROM Comment WHERE PostID = {postID}; ''')
                rows = cur.fetchall()
                comments = []
                for commentrow in rows:
                    comments.append(Comment(commentrow[0], commentrow[2], commentrow[1], commentrow[3], commentrow[4]))
                return comments
    def getCommentsByUserID(self, userID: int) -> list[Comment]:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT CommentID, PostID, Owner, Content, Timestamp FROM Comment WHERE Owner = '{userID}'; ''')
                rows = cur.fetchall()
                comments = []
                for commentrow in rows:
                    comments.append(Comment(commentrow[0], commentrow[2], commentrow[1], commentrow[3], commentrow[4]))
                return comments
    def createUserVoteOnPoll(self, userID: int, pollID: int, voteFor: bool) -> Vote: 
        time = datetime.now()
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''INSERT INTO Vote (Owner, PollID, VoteFor)
                                VALUES ({userID}, {pollID}, {voteFor}, {time}) RETURNING VoteID; ''')
                rows = cur.fetchall()
                return Vote(int(rows[0][0]), self.getUserByID(userID), pollID, voteFor, time)
            
    def getVoteByUserID(self, userID: str) -> Vote:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT VoteID, Owner, PollID, VoteFor, Timestamp FROM Vote WHERE Owner = '{userID}'; ''')
                rows = cur.fetchall()
                if cur.rowcount == 0:
                    return None
                return (Vote(rows[0][0], self.getUserByID(rows[0][1]), rows[0][2], rows[0][3], rows[0][4]))
                
    def getVotesForPoll(self, pollID: int) -> int:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT COUNT(*) FROM Vote WHERE PollID = {pollID} AND VoteFor = TRUE; ''')
                rows = cur.fetchall()
                return int(rows[0][0])
    def getVotesAgainstPoll(self, pollID: int) -> int:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT COUNT(*) FROM Vote WHERE PollID = {pollID} AND VoteFor = FALSE; ''')
                rows = cur.fetchall()
                return int(rows[0][0])
    def changeVote(self, voteID: int, voteFor: bool) -> Vote:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''UPDATE Vote SET VoteFor = {voteFor} WHERE VoteID = {voteID}; ''')
                return self.getVoteByVoteID(voteID)
    def getVoteByVoteID(self, voteID: int) -> Vote:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT VoteID, Owner, PollID, VoteFor, Timestamp FROM Vote WHERE VoteID = {voteID}; ''')
                rows = cur.fetchall()
                return Vote(rows[0][0], self.getUserByID(rows[0][1]), rows[0][2], rows[0][3], rows[0][4])
    def getCommentByCommentID(self, commentID: int) -> Comment:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT CommentID, Owner, PostID, Content, Timestamp FROM Comment WHERE CommentID = {commentID}; ''')
                rows = cur.fetchall()
                return Comment(rows[0][0], self.getUserByID(rows[0][1]), rows[0][2], rows[0][3], rows[0][4])
    def deleteVote(self, voteID: int) -> None:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''DELETE FROM Vote WHERE VoteID = {voteID}; ''')
    def deleteComment(self, commentID: int) -> None:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''DELETE FROM Comment WHERE CommentID = {commentID}; ''')
    def deletePost(self, postID: int) -> None:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''DELETE FROM Comment WHERE PostID = {postID}; ''')
                cur.execute(f'''DELETE FROM Post WHERE PostID = {postID}; ''')
    def deleteUser(self, userID: str) -> None:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'''DELETE FROM Vote WHERE Owner = '{userID}'; ''')
                cur.execute(f'''DELETE FROM Comment WHERE Owner = '{userID}'; ''')
                cur.execute(f'''DELETE FROM IMAGE WHERE Author = '{userID}'; ''')
                cur.execute(f'''DELETE FROM Post WHERE Owner = '{userID}'; ''')
                cur.execute(f'''DELETE FROM Users WHERE UserID = '{userID}'; ''')

    def searchPosts(self, query: str) -> list[Post]:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                # Use ILIKE for case-insensitive search and % for wildcard characters before and after the query
                cur.execute('SELECT PostID, Owner, Title, ImageID, TextContent, Timestamp FROM Post WHERE Title ILIKE %s', ('%' + query + '%',))
                rows = cur.fetchall()
                posts = []
                for postrow in rows:
                    posts.append(Post(postrow[0], postrow[1], postrow[2], postrow[3], postrow[4], postrow[5]))
                return posts
    def editPost(self, postID: int, text_content: str) -> Post:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'UPDATE Post SET TextContent = \'{text_content}\' WHERE PostID = {postID};')
                return self.getPostByID(postID)
    def editUser(self, userID: str, username: str) -> User:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'UPDATE Users SET Username = \'{username}\' WHERE UserID = \'{userID}\';')
                return self.getUserByID(userID)
    def editComment(self, commentID: int, content: str) -> Comment:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'UPDATE Comment SET Content = \'{content}\' WHERE CommentID = {commentID};')
                return self.getCommentByCommentID(commentID)
    def updateUsername(self, user_id, new_username):
        pool = get_pool()
        try:
            with pool.connection() as conn:
                with conn.cursor() as cursor:
                    # Execute a SQL update query to update the username
                    sql = "UPDATE Users SET Username = %s WHERE UserID = %s::VARCHAR"
                    cursor.execute(sql, (new_username, user_id))
                    # Commit the transaction
                    conn.commit()
            return True  # This should be inside the try block
        except Exception as e:
            print("Error updating username:", e)
            # Rollback the transaction in case of an error
            conn.rollback()
            return False
