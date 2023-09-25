from App.database import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String, nullable = False)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)

    student = db.relationship(Student, backref='students')

    def __init__(self, name):
        name=self.name
        karma=0

    def get_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'karma': self.karma
        }