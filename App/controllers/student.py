from App.models import Student
from App.database import db

def create_student(name):
    student = Student(name)
    db.session.add(student)
    db.session.commit()

    return


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