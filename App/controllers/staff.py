from App.models import User, Staff
from App.database import db

def create_staff(email,name,password):
    new_staff= Staff(email=email, name=name, password=password)

    db.session.add(new_staff)
    db.session.commit()
    
    return 

def get_staff_member(email):
    return Staff.query.filter_by(email=email).first()

def get_all_staff():
    return Staff.query.all()