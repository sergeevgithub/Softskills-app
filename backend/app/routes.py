from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from .models import User, Course
from .schemas import user_schema, course_schema, courses_schema
from . import db, bcrypt

routes = Blueprint('routes', __name__)

@routes.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

@routes.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'id': user.id, 'username': user.username})
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@routes.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    return courses_schema.jsonify(courses), 200

@routes.route('/courses', methods=['POST'])
@jwt_required()
def add_course():
    title = request.json.get('title')
    description = request.json.get('description')

    if not title or not description:
        return jsonify({'message': 'Title and description are required'}), 400

    new_course = Course(title=title, description=description)
    db.session.add(new_course)
    db.session.commit()

    return course_schema.jsonify(new_course), 201