from datetime import datetime
from puppycompanyblog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(100), nullable=False, default="default_profile.png")
    email = db.Column(db.String(100), unique=True, index=True)
    username = db.Column(db.String(100), unique=True, index=True)
    password_hash = db.Column(db.String(1024))

    posts = db.relationship("BlogPost", backref="author", lazy=True)

    def __init__(self, email: str, username: str, password: str):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f"{self.username}"


class BlogPost():

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tz = db.Column(db.String(100), nullable=False, default="UTC")
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    users = db.relationship(User)

    def __init__(self, title: str, text: str, user_id: str):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __str__(self):
        if not (self.text is None):
            return f"Post {self.id} (authorId {self.user_id}, {len(self.text)} characters)"
        else:
            return f"Post {self.id}"
