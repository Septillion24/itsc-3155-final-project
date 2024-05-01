from flask import Flask, abort, jsonify, redirect, render_template, request, url_for, session
from authlib.integrations.flask_client import OAuth
from classes.DataBaseHandler import DataBaseHandler
from classes.DataTypes import Post, User, Comment, Image
from dotenv import load_dotenv
from datetime import datetime
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
currentPollID = 1

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    logged_in = False
    if 'email' in session:
        logged_in = True
    return render_template('forum.html', logged_in=logged_in)

#account management

@app.route('/login')
def login():
    nonce = generate_nonce()
    session['nonce'] = nonce  # Store nonce in session for later validation
    redirect_url = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_url, nonce=nonce)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    try:
        id_token = google.parse_id_token(token, nonce=session.get('nonce'))
    except ValueError as e:
        print("Nonce mismatch or other token validation error:", e)
        return "Token validation error", 400
    
    user_id = id_token.get('sub')
    user = db.getUserByID(user_id)
    session['email'] = id_token.get('email')
    session['username'] = session['email'].split('@')[0]
    session['user_id'] = user_id
    session['authenticated'] = True
    if (user == None):
        db.createUser(
            userID= user_id,
            username=session['username'],
            email=session['email'],
            firstname=id_token.get('given_name'),
            lastname=id_token.get('family_name')
            )
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('forum.html')


#/forum

@app.get("/forum")
def forumPage():
    logged_in = session.get('authenticated', False)
    return render_template("forum.html", logged_in = logged_in)

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
    if session.get('authenticated',False) != True:
        return "Not authorized", 401
    
    user_id = session['user_id']
    title = request.post["title"]
    text_content = request.post["postContent"]
    image_url = request.post["imageURL"]
    image = db.createImage(url=image_url,author=user_id)
    print("Creating post: " + title + ", '" + text_content + "'")
    response = db.createPost(user_id,title,image_id=image, text_content=text_content)
    print(response)
    if response:
        return redirect(f"/forum/post/{response.post_id}")
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
    
    
#about
@app.get('/about')
def aboutPage():
    logged_in = session.get('authenticated', False)
    return render_template('about.html', logged_in = logged_in)


#voting
    
@app.post('/vote')
def castVote():
    if session.get('authenticated',False) != True:
        return "Not authorized", 401
    
    user_id = session['user_id']
    option = request.form['option']
    
    db.createUserVoteOnPoll(user_id, currentPollID, option == 'yes')
    
    
@app.get('/vote')
def votePage():
    logged_in = session.get('authenticated', False)
    return render_template('voting.html', votes = votes, logged_in = logged_in)

@app.route('/vote/previous', methods=['GET', 'POST'])
def indexPrevious():
    return render_template('previous.html')

@app.route('/vote/next', methods=['GET', 'POST'])
def indexNext():
    return render_template('next.html')

#maps

@app.get('/newsearch')
def newPostPage():
    logged_in = session.get('authenticated', False)
    return render_template('search.html', logged_in = logged_in)

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

            if elevation < 50:
                haunted = "Definitely Haunted"
            elif elevation < 200:
                haunted = "Probably Haunted"
            else:
                haunted = "Not Haunted (as far as we know)"
                
        else:
            elevation = 'Unknown'
            haunted = "Unknown"
        return render_template('result.html', location=location, lat=lat, lng=lng, elevation=elevation, haunted = haunted, googleKey = os.getenv('MapsKey', ''))
    else:
        return "Unsuccessful", 400



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