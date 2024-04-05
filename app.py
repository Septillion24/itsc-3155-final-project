from flask import Flask, abort, jsonify, redirect, render_template, request
from classes.DataBaseHandler import DataBaseHandler
from models import db, Discussion, Comment, User

app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
db = DataBaseHandler.getInstance()

# with app.app_context():
    # db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

def get_discussion_by_id(post_id):
    return Discussion.query.get(post_id)

def get_comments_for_discussion(post_id):
    return Comment.query.filter_by(post_id=post_id).all()

@app.route('/')
def index():
    return render_template("index.html")

@app.get('/signup')
def signupPage():
    return render_template("signup.html")

@app.route('/signup', methods = ['POST'])
def signup():
    userName = request.form['userName']
    passWord = request.form['passWord']  # TODO: set up 
    result = doSignInProcess()
    if result:    
        return redirect("/index")
    else:
        return "Failed to create an account", 400

@app.get('/login')
def loginPage():
    return render_template("login.html")

@app.route('/login', methods=['POST'])     
def login():
    userName = request.form['userName']
    passWord = request.form['passWord']  # TODO: set up OAuth2
    result = doLoginProcess()
    if result:    
        return redirect("/index")
    else:
        return "Failed to log in", 401    

@app.route("/forum/makepost", methods=['POST'])
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

@app.route('/forum/post/<int:post_id>')
def getPostFromID(post_id):
    discussion = db.getPostByID(post_id)
    if discussion is None:
        abort(404)
    return discussion, 200

@app.route('/user/<str:username>')
def getUserByID():
    pass

def seed_database():
    users = [
        User(username='User1', avatar_url="images/avatar1.png"),
        User(username='User2', avatar_url="images/avatar2.png")
    ]
    
    for user in users:
        if not User.query.filter_by(username=user.username).first():
            db.session.add(user)
    
    db.session.commit()
    
    discussions = [
        Discussion(title='Is this a confirmed paranormal site?', image_url="images/discussion_image1.jpg"),
        Discussion(title='UFO sighting discussion', image_url="images/discussion_image2.jpg")
    ]
    
    for discussion in discussions:
        db.session.add(discussion)
    
    db.session.commit()
    
    comments = [
        Comment(content='Interesting point about the site.', post_id=discussions[0].id, user_id=users[0].id),
        Comment(content='I have seen similar sightings!', post_id=discussions[1].id, user_id=users[1].id)
    ]
    
    for comment in comments:
        db.session.add(comment)
    
    db.session.commit()

@app.cli.command('seed-db')
def seed_db_command():
    """Seeds the database with initial data."""
    with app.app_context():
        if User.query.first() is None:
            seed_database()
            print('Database seeded.')
        else:
            print('Database already seeded.')

if __name__ == '__main__':
    app.run(debug=True)
    
    
def doLoginProcess():
    pass
def doSignInProcess():
    pass