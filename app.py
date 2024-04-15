from flask import Flask, abort, jsonify, redirect, render_template, request
from classes.DataBaseHandler import DataBaseHandler

app = Flask(__name__)


db = DataBaseHandler.getInstance()

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return redirect("/forum")

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

@app.get("/forum")
def forumPage():
    return render_template("forum.html")

@app.get("/forum/getposts")
def getPostsForForumPage():
    topPosts = getTopPosts()
    return jsonify()

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

@app.get("/forum/posts")
def getPosts():
    posts = db.getPosts()
    return jsonify(posts)

@app.get('/forum/post/<int:post_id>')
def getPostFromID(post_id):
    discussion = db.getPostByID(post_id)
    if discussion is None:
        abort(404)
    return discussion, 200

@app.get('/user/<str:username>')
def getUserByID():
    pass

@app.get('/voting')
def votingPage():
    return render_template('voting.html')

@app.post('/voting')


@app.get('/voting')
def votingPage():
    return render_template('voting.html')

# @app.post('/voting')


if __name__ == '__main__':
    app.run(debug=True)

    
    
def doLoginProcess():
    pass
def doSignInProcess():
    pass

def getTopPosts() -> list['Post']:
    pass