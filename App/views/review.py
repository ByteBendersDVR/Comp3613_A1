from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from App.controllers import (
    get_reviews,
    get_review,
    add_review,
    update_score
)

review_views = Blueprint('review_views', __name__)

@review_views.route('/review/<int:studentID>', methods=["GET","POST"])
def add_review(studentID):
    if route.methods == "POST":
        data = request.json
        add_review(data["review"], studentID)
        
        return jsonify(message=(f'Review added for student {studentID}.')), 200
    
    if route.methods == "GET":
        reviews = get_reviews(studentID)

        reviews_json = [review.get_json for review in reviews]

        return jsonify(reviews_json), 200

@review_views.route('/vote/<int:reviewID>', methods=["POST"])
@jwt_required()
def voteOnReview(reviewID):
    data = request.json

    if data["vote"] == "+": 
        score_point = 1
    else:
        score_point = -1
    
    update_score(reviewID, score_point)

    return jsonify(message=(f'Vote of {score_point} added.')), 200
