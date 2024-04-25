from flask import Flask, abort, jsonify, redirect, render_template, request
from classes.DataBaseHandler import DataBaseHandler
from classes.DataTypes import Post, User, Comment
import requests
import random

app = Flask(__name__)

db = DataBaseHandler.getInstance()

MapsKey = 'AIzaSyBkaqZWoj0HgduAKegpLcz0NRfZ4iIg_JY'
votes = {'yes': 0, 'no': 0}

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
    topPosts = db.getTopPosts(numPosts)
    return jsonify([post.to_dict() for post in topPosts]), 200

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
    posts = db.getPostsByUserID(userID)
    return jsonify(posts)
@app.get("/user/<int:userID>/comments")
def getCommentsByUserID(userID:int):
    posts = db.getCommentsByUserID(userID)
    return jsonify(posts)
    
    
#voting

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        option = request.form['option']
        if option == 'yes':
            votes['yes'] += 1
        elif option == 'no':
            votes['no'] += 1
    return render_template('voting.html', votes=votes)

#maps

@app.get('/newsearch')
def newPostPage():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    location = request.form['location']

    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={MapsKey}'

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        elevation_url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lng}&key={MapsKey}'
        elevation_response = requests.get(elevation_url)
        elevation_data = elevation_response.json()
        if elevation_data['status'] == 'OK':
            elevation = elevation_data['results'][0]['elevation']
        else:
            elevation = 'Unknown'
        haunted = random.choice(["Definitely Haunted", "Probably Haunted", "Not Haunted (as far as we know)"])
        return render_template('result.html', location=location, lat=lat, lng=lng, elevation=elevation, haunted = haunted)
    else:
        return 400, "Unsuccessful"



if __name__ == '__main__':
    app.run(debug=True)

    
def doLoginProcess():
    pass
def doSignInProcess():
    pass

def getTopPosts(numPosts:int) -> list[Post]:
    pass