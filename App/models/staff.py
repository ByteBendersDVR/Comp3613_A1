from App.database import db
from .user import User

class Staff(User):
    __mapper_args__ = {
        "polymorphic_identity": "staff",
    }

    def __init__(self, name, email, password):
        super().__init__(name, email, password)

    def get_json(self):
        return super().get_json()
