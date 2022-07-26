from . import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Employee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    short_info = db.Column(db.String, nullable=False)
    experience = db.Column(db.Integer(), nullable=False)
    preferred_position = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("index", lazy=True))

    def __repr__(self):
        return f"Employee {self.name}"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = bcrypt.generate_password_hash(password_to_hash).decode("utf-8")

    def check_password(self, password_to_check):
        return bcrypt.check_password_hash(self.password_hash, password_to_check)