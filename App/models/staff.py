from App.database import db
from .user import User

class CetlUser(User):
    __mapper_args__ = {
        "polymorphic_identity": "cetl",
    }

    def __init__(self, name, email, password):
        super().__init__(name, email, password)

    def get_json(self):
        super().get_json()