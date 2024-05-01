from flask import Flask, abort, jsonify, redirect, render_template, request, url_for, session
from authlib.integrations.flask_client import OAuth
from classes.DataBaseHandler import DataBaseHandler
from classes.DataTypes import Post, User, Comment
from dotenv import load_dotenv
import requests
import base64
import random
import os

app = Flask(__name__)
load_dotenv()

app.secret_key = 'secret_key'

db = DataBaseHandler.getInstance()


oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('ClientID', ''),
    client_secret=os.getenv('ClientSecret', ''),
    # authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    # access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
)



votes = {'yes': 0, 'no': 0}

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    email = session.get('email')
    print(email) #remove later
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

@app.route('/login')
def login():
    nonce = generate_nonce()
    session['nonce'] = nonce  # Store nonce in session for later validation
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    try:
        id_token = google.parse_id_token(token, nonce=session.get('nonce'))
    except ValueError as e:
        print("Nonce mismatch or other token validation error:", e)
        return "Token validation error", 400
    
    user_info = id_token
    session['email'] = user_info.get('email')
    return redirect('/')

# @app.post('/login')
# def login():
#     username = request.form['username']
#     password = request.form['password']  # TODO: set up OAuth2
#     result = doLoginProcess()
#     if result:
#         return redirect("/index")
#     else:
#         return "Failed to log in", 401    

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
        if option == 'yes': # we will fix this later
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

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={os.getenv('MapsKey', '')}"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        elevation_url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lng}&key={os.getenv('MapsKey', '')}"
        elevation_response = requests.get(elevation_url)
        elevation_data = elevation_response.json()
        if elevation_data['status'] == 'OK':
            elevation = elevation_data['results'][0]['elevation']
        else:
            elevation = 'Unknown'
        haunted = random.choice(["Definitely Haunted", "Probably Haunted", "Not Haunted (as far as we know)"])
        return render_template('result.html', location=location, lat=lat, lng=lng, elevation=elevation, haunted = haunted, googleKey = os.getenv('MapsKey', ''))
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

def generate_nonce(length=16):
    return base64.urlsafe_b64encode(os.urandom(length)).decode('utf-8')