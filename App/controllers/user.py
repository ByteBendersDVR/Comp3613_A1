from App.models import User
from App.database import db

def create_user(email, name, password):
    newuser = User(email=email,name=name, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_name(name):
    return User.query.filter_by(name=name).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.name = username
        db.session.add(user)
        return db.session.commit()
    return None
    