from App.database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    karma = db.Column(db.Integer, nullable = False)

    def __init__(self, name):
        name=self.name
        karma=0

    def get_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'karma': self.karma
        }