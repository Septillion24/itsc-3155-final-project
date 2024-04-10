from flask import Flask, abort, redirect, render_template, request
from models import db, Discussion, Comment, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

def get_discussion_by_id(discussion_id):
    return Discussion.query.get(discussion_id)

def get_comments_for_discussion(discussion_id):
    return Comment.query.filter_by(discussion_id=discussion_id).all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/test1')
def test1():
    return render_template("index.html", test1=True)

@app.route('/test2')
def test2():
    return render_template("index.html", test2=True)

@app.route('/test3')
def test3():
    return render_template("index.html", test3=True)

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/forum/discussion/<int:discussion_id>')
def forum_discussion(discussion_id):
    discussion = get_discussion_by_id(discussion_id)
    if discussion is None:
        abort(404)
    
    comments = get_comments_for_discussion(discussion_id)
    
    comments_formatted = [
        {
            'username': comment.user.username,
            'avatar_url': comment.user.avatar_url,
            'content': comment.content
        } for comment in comments
    ]
    
    return render_template("forum.html", discussion=discussion, comments=comments_formatted)

@app.get('/voting')
def votingPage():
    return render_template('voting.html')

@app.post('/voting')


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
        Comment(content='Interesting point about the site.', discussion_id=discussions[0].id, user_id=users[0].id),
        Comment(content='I have seen similar sightings!', discussion_id=discussions[1].id, user_id=users[1].id)
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
