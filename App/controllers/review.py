from App.models import Review, Student
from .student import *
from App.database import db

def get_reviews(student_id):
    return Review.query.filter_by(student_id=student_id).all()

def get_review(student_id, review_id):
    return Review.query.filter_by(id=review_id, student_id=student_id).first()

def add_review(review, student_id):
    new_review = Review(review=review, student_id=student_id)

    db.session.add(new_review)
    db.session.commit()

    return

def update_score(review_id, score_point):
    review = Review.filter_by(id=review_id).first()

    review.score = review.score+score_point
    change_karma(review.student_id, score_point)

    db.session.add(review)
    db.session.commit()

    return