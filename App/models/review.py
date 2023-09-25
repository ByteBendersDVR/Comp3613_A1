from App.database import db
from .student import Student

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String, nullable = False)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    student = db.relationship(Student, backref='students')

    def __init__(self, review, student_id):
        self.review = review
        self.student_id = student_id
        self.score = 0

    def get_json(self):
        return{
            'id': self.id,
            'review' : self.review,
            'student_id' : self.student_id,
            'score' : self.score
        }
