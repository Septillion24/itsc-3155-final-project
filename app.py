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




currentPollID = 1

if __name__ == '__main__':
    app.run(debug=True)


@app.context_processor
def inject_variables():
    return {'template_user': db.getUserByID(session.get('user_id', -1))}

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
    return redirect('/')


#/forum

@app.get("/forum")
def forumPage():
    logged_in = session.get('authenticated', False)
    return render_template("forum.html", logged_in = logged_in)

@app.get("/forum/getposts")
def getPostsForForumPage():
    numPosts = request.args.get('numPosts', default=10, type=int)
    topPosts = db.getTopPosts(numPosts)
    for post in topPosts:
        postOwner = db.getUserByID(post.owner)
        post.owner_name = postOwner.first_name + " " + postOwner.last_name
    return jsonify([post.to_dict() for post in topPosts]), 200

@app.get('/forum/post/<int:post_id>')
def getPostFromID(post_id):
    post = db.getPostByID(post_id)
    user_id = session.get('user_id', None)
    
    if post is None:
        abort(404)

    if post.owner == user_id:
        owner = True
    else:
        owner = False

    logged_in = session.get('authenticated', False)
    return render_template("singlePost.html", post=post, logged_in=logged_in, owner = owner, user_id = user_id)

@app.post("/forum/makepost")
def createPost():
    if session.get('authenticated',False) != True:
        return "Not authorized", 401
    
    user_id = session['user_id']
    title = request.form["title"]
    text_content = request.form["postContent"]
    image_url = request.form["imageURL"]
    image = db.createImage(url=image_url,author=user_id)
    response = db.createPost(user_id,title,image=image, text_content=text_content, timestamp=datetime.now())
    if response:
        return redirect(f"/forum/post/{response.post_id}")
    else:
        return "Failed to create post", 400

@app.post("/forum/makeComment")
def createComment():
    if session.get('authenticated',False) != True:
        return "Not authorized", 401
    
    user_id = session['user_id']
    commentContent = request.form["commentContent"]
    postID = request.form["postID"]
    post = db.getPostByID(postID)
    if post == None:
        return "No post found with that ID", 404
    owner = db.getUserByID(user_id)
    db.createComment(post,owner,commentContent, datetime.now())
    return redirect(f'/forum/post/{postID}')

@app.get("/forum/<int:postID>/comments")
def getCommentsOnPost(postID):
    comments = db.getCommentsByPostID(postID)
    for comment in comments:
        commentOwner = db.getUserByID(comment.owner)
        comment.owner_name = commentOwner.first_name + " " + commentOwner.last_name
    return jsonify([comment.to_dict() for comment in comments])

#about

@app.get('/about')
def getAbout():
    logged_in = session.get('authenticated', False)
    return render_template("about.html", logged_in = logged_in)

#/user

@app.get('/user/<int:userID>')
def getUserByID(userID:int):
    user = db.getUserByID(userID)
    logged_in = session.get('authenticated', False)
    user_id = session['user_id']
    owner = userID == user_id
    return render_template("user.html", user=user, logged_in = logged_in, owner=owner)

@app.get("/user/<int:userID>/posts")
def getPostsByUserID(userID:int):
    posts = db.getPostsByUserID(userID)
    for post in posts:
        postOwner = db.getUserByID(post.owner)
        post.owner_name = postOwner.first_name + " " + postOwner.last_name
    return jsonify([post.to_dict() for post in posts]), 200

@app.get("/user/<int:userID>/comments")
def getCommentsByUserID(userID:int):
    posts = db.getCommentsByUserID(userID)
    return jsonify([post.to_dict() for post in posts])
    
#voting
    
@app.post('/vote')
def castVote():
    logged_in = session.get('authenticated', False)
    if session.get('authenticated',False) != True:
        return "Not authorized", 401
    
    user_id = session['user_id']
    option = request.form['option']

    vote = db.getVoteByUserID(user_id)

    if (vote != None):
        db.changeVote(vote.vote_id, option == 'yes')
        vote = db.getVoteByUserID(user_id)
    else:
        print("adding new vote")
        vote = db.createUserVoteOnPoll(user_id, currentPollID, option == 'yes')
        
    
    votes = {'yes': db.getVotesForPoll(1), 'no': db.getVotesAgainstPoll(1)}
    
    return render_template('voting.html', votes = votes, logged_in = logged_in, uservote=vote)
    
    
@app.get('/vote')
def votePage():
    votes = {'yes': db.getVotesForPoll(1), 'no': db.getVotesAgainstPoll(1)}
    
    logged_in = session.get('authenticated', False)
    return render_template('voting.html', votes = votes, logged_in = logged_in)

@app.get('/vote/next')
def nextPage():
    logged_in = session.get('authenticated', False)
    return render_template('next.html', logged_in = logged_in)

@app.get('/vote/previous')
def previousPage():
    logged_in = session.get('authenticated', False)
    return render_template('previous.html', logged_in = logged_in)


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


#deleting

@app.post('/delete/post')
def deletePost():
    if session.get('authenticated', False) != True:
        return "Not authorized", 401
    
    user_id = session['user_id']
    postID = request.json['postID']
    
    if db.getPostByID(postID).owner != user_id:
        return "Not authorized", 401
    try:
        db.deletePost(postID)
        return "Successfully deleted", 200
    
    except Exception as e:
        print(e)
        return "Could not delete post", 400

@app.post('/delete/comment')
def deleteComment():
    if session.get('authenticated', False) != True:
        return "Not authorized", 401
    
    user_id = session['user_id']
    commentID = request.json["commentID"]
    
    if db.getCommentByCommentID(commentID).owner.user_id != user_id:
        return "Not authorized", 401
    try:
        db.deleteComment(commentID)
        return "Successfully deleted", 200
    
    except Exception as e:
        print(e)
        return "Could not delete comment", 400

@app.post('/delete/user')
def deleteUser():
    if session.get('authenticated', False) != True:
        return "Not authorized", 401
    
    user_id = session['user_id']
    deletedUserID = request.json["userID"]
    
    if deletedUserID != user_id:
        return "Not authorized", 401
    try:
        for post in db.getPostsByUserID(deletedUserID):
            db.deletePost(post.post_id)
        for comment in db.getCommentsByUserID(deletedUserID):
            db.deletePost(comment.comment_id)
        
        db.deleteUser(deletedUserID)
        session.clear()
        return "Successfully deleted", 200
    
    except Exception as e:
        print(e)
        return "Could not delete user", 400

# editing
@app.post('/edit/post')
def editPost():
    if session.get('authenticated', False) != True:
        return "Not authorized", 401
    
    user_id = session['user_id']
    postID = request.json['postID']
    post = db.getPostByID(postID)
    if post == None:
        return "Post not found", 404
    if post.owner != user_id:
        return "Not authorized", 401
    
    newContent = request.json['newContent']
    db.editPost(postID, newContent)
    
    return redirect(f'/forum/post/{postID}')
    
    
@app.post('/edit/comment')
def editComment():
    if session.get('authenticated', False) != True:
        return "Not authorized", 401
    
    user_id = session['user_id']
    commentID = request.json["commentID"]
    comment = db.getCommentByID(commentID)
    if comment == None:
        return "Comment not found", 404
    if comment.owner != user_id:
        return "Not authorized", 401
    
    newContent = request.json['newContent']
    db.editComment(commentID, newContent)
    
    
    
    
@app.post('/edit/user')
def editUser():
    if session.get('authenticated', False) != True:
        return "Not authorized", 401
    
    user_id = session['user_id']
    editedUserID = request.json["userID"]
    
    if editedUserID != user_id:
        return "Not authorized", 401
    
    newUsername = request.json['newUsername']
    db.editUser(editedUserID, newUsername)
    
    

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

@app.route('/search_results')
def search_results():
    search_query = request.args.get('search_query', '')
    print(f"Searching for posts with query: {search_query}")
    if search_query:
        posts = db.searchPosts(search_query)
        print(f"Found posts: {posts}")
        return render_template('search_results.html', posts=posts)
    else:
        return render_template('search_results.html', posts=[], error="No search term provided.")