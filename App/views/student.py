from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from App.controllers import *

student_views = Blueprint('student_views', __name__)

# this retrieves all students
@student_views.route('/students', methods=["GET"])
def getStudents():
    students = get_all_students()

    if students:
        students_json = [student.get_json() for student in students]
        return jsonify(students_json), 200

    return jsonify("Error retrieving students."), 401

# this retrieves a particular student
@student_views.route('/students/<int:id>', methods=["GET"])
def getParticularStudent(id):
    student = get_student(id)

    if student:
        students_json = student.get_json()
        return jsonify(students_json), 200
    
    return jsonify(message=(f'Student with id:{id} could not be found.')), 401

# this adds a new student, user must be logged in 
@student_views.route('/addstudent', methods=["POST"])
@jwt_required()
def addStudent():
    data = request.json

    student = create_student(data["name"])

    return jsonify(message=(f'Student was created with id:{student}.')), 200

# this updates a student, user must be logged in
@student_views.route('/updatestudent/<int:id>', methods=["PUT"])
@jwt_required()
def updateStudent(id):
    data = request.json

    if update_student(id, data):
        return jsonify(message=(f'Student with id:{id} was updated.')), 200
    
    return jsonify(message=(f'Error in updating student with id:{id}')), 401





