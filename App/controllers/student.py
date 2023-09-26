from App.models import Student
from App.database import db

def create_student(name):
    student = Student(name)
    db.session.add(student)
    db.session.commit()

    return student.id


def get_all_students():
    return Student.query.all()

def get_student(id):
    return Student.query.filter_by(id=id).first()

def change_karma(student_id, karma):
    student = Student.query.filter_by(id=student_id).first()

    student.karma = student.karma+karma

    db.session.add(student)
    db.session.commit()

    return

# This takes the new_data from the request, checks which fields are in it and update
# the appropriate field from the student object, given a student_id
def update_student(student_id, new_data):
    student = get_student(student_id)
    
    for field in ("name", "karma"):
        if field in new_data:
            setattr(student, field, new_data[field])

    db.session.commit()

    return True