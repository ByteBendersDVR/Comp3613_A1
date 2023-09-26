from App.database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    karma = db.Column(db.Integer, nullable = False)
    # studentID = db.Column(db.Integer, nullable = False, unique=True)
    
    def __init__(self, name):
        self.name=name
        self.karma=0

    def get_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'karma': self.karma
        }