import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Staff, Student, Review
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''

class UnitTests(unittest.TestCase):
# name, email, pw, user_type
    def test_new_user(self):
        user = User(name="bob",email="bob@gmail.com", password="bobpass")
        assert user.name == "bob"

    # pure function no side effects or integrations called
    # def test_get_json(self):
    #     user = User(name="bob",email="bob@mail.com", password="bobpass", user_type="superadmin")
    #     user_json = user.get_json()
    #     self.assertDictEqual(user_json, {"id":None, "name":"bob", "email":"bob@mail.com"})
    
    def test_new_staff(self):
        staff = Staff(name="rich", email="rich@mail.com", password="richpass")
        db.session.add(staff)
        db.session.commit()
        newStaff = get_staff_member(staff.email)
        assert newStaff.name == "rich"

    def test_get_user(self):
        user = User(name="bob",email="bob@mail.com", password="bobpass")
        db.session.add(user)
        db.session.commit()
        getting_user = User.query.filter_by(email="bob@mail.com").first()
        self.assertDictEqual(getting_user.get_json(), {"id":1, "name":"bob", "email":"bob@mail.com"})

    def test_create_student(self):
        student = Student(name="masud")
        db.session.add(student)
        db.session.commit()
        new_student = Student.query.filter_by(name="masud").first()
        assert new_student.name == "masud"

    # Not doing these for now
    # def test_hashed_password(self):
    #     password = "mypass"
    #     hashed = generate_password_hash(password, method='sha256')
    #     user = User("bob", password)
    #     assert user.password != password

    # def test_check_password(self):
    #     password = "mypass"
    #     user = User("bob", password)
    #     assert user.check_password(password)



'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


# def test_authenticate():
#     user = create_user("bob", "bobpass")
#     assert login("bob", "bobpass") != None

class IntegrationTests(unittest.TestCase):

    # def test_create_user(self):
    #     user = create_user("rick", "bobpass")
    #     assert user.username == "rick"

    # def test_get_all_users_json(self):
    #     users_json = get_all_users_json()
    #     self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # # Tests data changes in the database
    # def test_update_user(self):
    #     update_user(1, "ronnie")
    #     user = get_user(1)
    #     assert user.username == "ronnie"

    def test_get_students(self):
        studentID = create_student("masud")
        studentID2 = create_student("morty")
        
        students = get_all_students()
        assert students is not None
        
    def test_update_student(self):
        studentID = create_student("masud")
        new_student_name = {
            "name": "rick"
        }
        update_student(studentID, new_student_name) 
        updated_student = get_student(studentID)
        assert updated_student.name == "rick"

    def test_create_review(self):
        studentID = create_student("masud")
        review = "They were great"
        new_review = create_review(review, studentID)
        created_review = get_review(studentID, new_review)

        assert created_review.review == review
        
 
    def test_get_reviews(self):
        studentID = create_student("masud")
        review = "They were great"
        create_review(review, studentID)
        reviews = get_reviews(studentID)

        assert reviews is not None
    
    def test_upvote_review(self):
        studentID = create_student("masud")
        review = "They were great"
        new_reviewID = create_review(review, studentID)
        acquiredReview = get_review(studentID, new_reviewID)
        old_score = acquiredReview.score

        update_score(acquiredReview.id, 7)
        updated_review = get_review(studentID, acquiredReview.id)
        new_score = updated_review.score

        if new_score > old_score:
            updated = True
        else:
            updated = False

        self.assertTrue(updated, "Score was not updated successfully.")
    
