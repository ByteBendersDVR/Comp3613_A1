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
        user = User(name="bob",email="bob@gmail.com", password="bobpass", user_type="superadmin")
        assert user.name == "bob"

    # pure function no side effects or integrations called
    # def test_get_json(self):
    #     user = User(name="bob",email="bob@mail.com", password="bobpass", user_type="superadmin")
    #     user_json = user.get_json()
    #     self.assertDictEqual(user_json, {"id":None, "name":"bob", "email":"bob@mail.com"})
    
    def test_new_staff(self):
        staff = Staff(name="rich", email="rich@mail.com", password="richpass")
        new_staff = Staff.query.filter_by(email="rich@mail.com").first()
        assert new_staff.name == "rich"

    def test_get_user(self):
        user = User(name="rich", email="rich@mail.com", password="richpass", user_type="staff")
        getting_user = User.query.filter_by(email="rich@gmail.com").first()
        self.assertDictEqual(user_json, {"id":None, "name":"rich", "email":"rich@mail.com"})

    def test_create_student(self):
        student = Student(name="masud")
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
        students = get_all_students()
        
        try:
            data = json.loads(students)
            is_valid_json = True
        except json.JSONDecodeError:
            is_valid_json = False

        self.assertTrue(is_valid_json, "Valid JSON object was not returned")

    def test_update_student(self):
        student = get_student(1)  
        new_student_name = "rick"
        update_student(1, new_student_name)    #should be masud if previous test stores within testing db
        updated_student = get_student(1)
        assert update_student.name == "rick"

    def test_create_review(self):
        student = get_student(1) #assuming it uses already created student
        review = "They were great"
        new_review = Review(review=review, student_id=student.id)
        created_review = get_review(student.id, new_review.id)

        try:
            check_review = json.loads(created_review)
            is_valid_json = True
        except json.JSONDecodeError:
            is_valid_json = False

        self.assertTrue(is_valid_json, "Valid JSON object was not returned")
 
    def test_get_reviews(self):
        student = get_student(1)
        reviews = get_reviews(student.id)

        try:
            check_reviews = json.loads(reviews)
            is_valid_json = True
        except json.JSONDecodeError:
            is_valid_json = False

        self.assertTrue(is_valid_json, "Valid JSON object was not returned")
 
    def test_upvote_review(self):
        student = get_student(1)
        review = get_review(student.id)
        old_score = review.score

        update_score(review.id, 7)
        updated_review = get_review(student.id)
        new_score = updated_review.score

        if new_score > old_score:
            updated = True
        else:
            updated = False

        self.assertTrue(updated, "Score was not updated successfully.")
    '''
