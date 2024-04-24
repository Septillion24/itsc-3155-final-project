from flask import Flask, abort, jsonify, redirect, render_template, request
from classes.DataBaseHandler import DataBaseHandler
from classes.DataTypes import Post, User, Comment

app = Flask(__name__)

db = DataBaseHandler.getInstance()

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return redirect("/forum")

#account management

@app.get('/signup')
def signupPage():
    return render_template("signup.html")

@app.post('/signup')
def signup():
    username = request.form['username']
    password = request.form['password']  # TODO: set up 
    result = doSignInProcess()
    if result:    
        return redirect("/index")
    else:
        return "Failed to create an account", 400

@app.get('/login')
def loginPage():
    return render_template("login.html")

@app.post('/login')
def login():
    username = request.form['usermame']
    password = request.form['password']  # TODO: set up OAuth2
    result = doLoginProcess()
    if result:    
        return redirect("/index")
    else:
        return "Failed to log in", 401    

#/forum

@app.get("/forum")
def forumPage():
    return render_template("home_jinja.html")

@app.get("/forum/getposts")
def getPostsForForumPage():
    numPosts = request.args.get('numPosts', default=10, type=int)
    topPosts = getTopPosts(numPosts)
    return jsonify(topPosts), 200

@app.get('/forum/post/<int:post_id>')
def getPostFromID(post_id):
    discussion = db.getPostByID(post_id)
    if discussion is None:
        abort(404)
    return discussion, 200

@app.post("/forum/makepost")
def createPost():
    title = request.post["title"]
    postContent = request.post["postContent"]
    user = request.post["user"] #TODO: authentication
    response = db.createPost(user,title,postContent)
    if response:
        return "OK", 200
    else:
        return "Failed to create post", 400


#/user

@app.get('/user/<int:userID>')
def getUserByID(userID:int):
    user = db.getUserByID(userID)
    return render_template("user.html", user=user)
@app.get("/user/<int:userID>/posts")
def getPostsByUserID(userID:int):
    posts = db.getPostsByUserID(userID) # TODO: implement this
    return jsonify(posts)
    
#voting

@app.get('/voting')
def votingPage():
    activeVote = db.getActiveVote()
    return render_template('voting.html', activeVote=activeVote)

@app.post('/voting/submitvote')
def submitVote():
    """
        'selection': boolean -- Either yes or no for the vote.
        'pollID': int -- The poll that is being voted on
        'userID': int -- The id for the user that is voting
    """
    pollID = request.form['pollID']
    userID = request.form['userID']
    selection = request.form['selection']
    authstuff = None #placeholder for oauth stuff so i dont forget later
    status = db.createUserVoteOnPoll(pollID,userID, selection) # TODO: implement this
    
    if status:
        return 200, "Poll vote successfully submitted"
    else:
        return 400, "Poll vote unsuccessful"



if __name__ == '__main__':
    app.run(debug=True)

    
def doLoginProcess():
    pass
def doSignInProcess():
    pass

def getTopPosts(numPosts:int) -> list[Post]:
    pass