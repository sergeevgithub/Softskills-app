from flask import Blueprint, jsonify, request, redirect
from flask_jwt_extended import jwt_required, create_access_token
from flask import send_from_directory
import re
import bcrypt

import mariadb

routes = Blueprint('routes', __name__)


# Helper function to connect to MariaDB
def get_db_connection(database='users_db',
                      user='guest',
                      password='12345',
                      host='localhost',
                      port=3306):
    DB_CONFIG = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': database
    }

    try:
        connection = mariadb.connect(**DB_CONFIG)
        return connection
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None


@routes.route('/<path:path>', methods=['GET'])
def static(path):
    return send_from_directory('../frontend/public', path)


@routes.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    connection = get_db_connection()

    if not connection:
        return jsonify({'message': 'Database connection failed'}), 503

    cursor = connection.cursor(dictionary=True)

    try:
        table_name = 'users_info'
        # Check if the account already exists
        cursor.execute(f'SELECT * FROM {table_name} WHERE user_name = ?', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            # Hash the password before storing it
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(f'INSERT INTO {table_name} (user_name, password) VALUES (?, ?)',
                           (username, hashed_password.decode('utf-8')))
            connection.commit()
            msg = 'You have successfully registered!'
    except mariadb.Error as e:
        print(f"Error querying database: {e}")
        return jsonify({'message': 'Database error occurred'}), 503
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': msg}), 201


@routes.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    connection = get_db_connection()

    if not connection:
        return jsonify({'message': 'Database connection failed'}), 503

    cursor = connection.cursor(dictionary=True)

    try:
        table_name = 'users_info'
        cursor.execute(f'SELECT * FROM {table_name} WHERE user_name = ?', (username,))
        account = cursor.fetchone()
    except mariadb.Error as e:
        print(f"Error querying database: {e}")
        account = None
    finally:
        cursor.close()
        connection.close()

    if account:
        # Verify the password using bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), account['password'].encode('utf-8')):
            msg = 'Logged in successfully!'
        else:
            return jsonify({'message': 'Incorrect username/password!'}), 401
    else:
        return jsonify({'message': 'Incorrect username/password!'}), 401

    return jsonify({'message': msg}), 201


@routes.route('/study_plan')
def get_study_plan():
    return jsonify({
        "study_plan": [
            {"day_number": 1, "topic": "Understanding Conflict", "available": True},
            {"day_number": 2, "topic": "Conflict Causes and Triggers", "available": False},
            {"day_number": 3, "topic": "Conflict Response Styles", "available": False},
            {"day_number": 4, "topic": "Active Listening", "available": False},
            {"day_number": 5, "topic": "Non-Verbal Communication", "available": False},
            {"day_number": 6, "topic": "Assertive Communication", "available": False},
            {"day_number": 7, "topic": "Emotional Regulation", "available": False},
            {"day_number": 8, "topic": "Negotiation Fundamentals", "available": False},
            {"day_number": 9, "topic": "Conflict Resolution Strategies", "available": False}
        ]})


@routes.route('/day_plan')
def get_day_plan():
    day = request.json.get('day_number')
    course_id = request.json.get('course_id')

    if not day or not course_id:
        return jsonify({'message': 'Course id and day are required', 'activities_number': 3}), 400

    connection = get_db_connection('courses_db')

    if not connection:
        return jsonify({'message': 'Database connection failed', 'activities_number': 3}), 503

    cursor = connection.cursor(dictionary=True)

    try:
        table_name = 'study_plan'
        cursor.execute(f'SELECT * FROM {table_name} WHERE (course_id = ? AND day = ?)', (course_id, day))
        sp_id = cursor.fetchone()['id']

        table_name = 'activities'
        cursor.execute(f'SELECT * FROM {table_name} WHERE sp_id = ?', (sp_id))
        activities = cursor.fetchall()
    except mariadb.Error as e:
        print(f"Error querying database: {e}")
        activities = None
    finally:
        cursor.close()
        connection.close()

    if activities:
        return jsonify({'message': 'There are some activities', 'activities_number': len(activities)}), 201

    return jsonify({'message': 'No activities', 'activities_number': 3}), 401

@routes.route('/theory')
def get_theory():
    # day = request.json.get('day_number')
    # course_id = request.json.get('course_id')
    #
    # if not day or not course_id:
    #     return jsonify({'message': 'Course id and day are required', 'content': ''}), 400
    #
    # connection = get_db_connection('courses_db')
    #
    # if not connection:
    #     return jsonify({'message': 'Database connection failed', 'content': ''}), 503
    #
    # cursor = connection.cursor(dictionary=True)
    #
    # try:
    #     table_name = 'study_plan'
    #     cursor.execute(f'SELECT * FROM {table_name} WHERE (course_id = ? AND day = ?)', (course_id, day))
    #     sp_id = cursor.fetchone()['id']
    #
    #     table_name = 'theories'
    #     cursor.execute(f'SELECT * FROM {table_name} WHERE sp_id = ?', (sp_id))
    #     theory_content = cursor.fetchone()['body']
    # except mariadb.Error as e:
    #     print(f"Error querying database: {e}")
    #     theory_content = None
    # finally:
    #     cursor.close()
    #     connection.close()
    #
    # if theory_content:
    #     return jsonify({'message': 'There are some theory', 'content': theory_content}), 201
    #
    # return jsonify({'message': 'No content', 'content': ''}), 401
    return jsonify(
        {
            "coreConcept": "Conflict happens naturally in life. It’s when people, groups, or even a person within themselves have disagreements, tensions, or don’t see things the same way.",
            "typesOfConflicts": [
                {
                    "type": "Interpersonal Conflicts",
                    "description": "Conflicts between two or more people.",
                    "causes": [
                        "Different ways of communicating",
                        "Different personal goals",
                        "Different expectations",
                        "Different values"
                    ]
                },
                {
                    "type": "Intrapersonal Conflicts",
                    "description": "Conflicts that happen inside yourself.",
                    "involves": [
                        "Struggles with personal values",
                        "Having a hard time making decisions",
                        "Feeling torn between emotions and logical thinking"
                    ]
                },
                {
                    "type": "Organizational Conflicts",
                    "description": "Conflicts that happen at work or in an organization.",
                    "triggers": [
                        "Fighting over resources",
                        "Not being clear about roles",
                        "Changes in the organization",
                        "Pressure to perform well"
                    ]
                },
                {
                    "type": "Structural Conflicts",
                    "description": "Conflicts caused by how an organization is set up.",
                    "characteristics": [
                        "Barriers between levels of management",
                        "Problems with communication",
                        "Strict or slow processes"
                    ]
                },
                {
                    "type": "Value-Based Conflicts",
                    "description": "Conflicts caused by differences in beliefs or values.",
                    "involves": [
                        "Disagreeing on ethics or morals",
                        "Different cultural perspectives",
                        "Conflicts over ideologies"
                    ]
                }
            ],
            "conflictDynamics": {
                "constructiveConflicts": {
                    "description": "Conflicts that lead to positive outcomes.",
                    "benefits": [
                        "Help people understand each other better",
                        "Encourage new ideas and solutions",
                        "Bring about positive change"
                    ]
                },
                "destructiveConflicts": {
                    "description": "Conflicts that lead to negative outcomes.",
                    "effects": [
                        "Create bad feelings",
                        "Stop people from solving problems",
                        "Hurt relationships"
                    ]
                }
            }
        }
    )

@routes.route('/activity')
def get_activity():
    # day = request.json.get('day_number')
    # course_id = request.json.get('course_id')
    # number_act = request.json.get('number_act')
    #
    # if not day or not course_id or not number_act:
    #     return jsonify({'message': 'Course id, activities number and day are required', 'content': ''}), 400
    #
    # connection = get_db_connection('courses_db')
    #
    # if not connection:
    #     return jsonify({'message': 'Database connection failed', 'content': ''}), 503
    #
    # cursor = connection.cursor(dictionary=True)
    #
    # try:
    #     table_name = 'study_plan'
    #     cursor.execute(f'SELECT * FROM {table_name} WHERE (course_id = ? AND day = ?)', (course_id, day))
    #     sp_id = cursor.fetchone()['id']
    #
    #     table_name = 'activities'
    #     cursor.execute(f'SELECT * FROM {table_name} WHERE (sp_id = ? and number = ?)', (sp_id, number_act))
    #     activities_content = cursor.fetchone()['body']
    # except mariadb.Error as e:
    #     print(f"Error querying database: {e}")
    #     activities_content = None
    # finally:
    #     cursor.close()
    #     connection.close()
    #
    # if activities_content:
    #     return jsonify({'message': 'There are som e activities', 'content': activities_content}), 201
    #
    # return jsonify({'message': 'No content', 'content': ''}), 401
    return jsonify(
        {
            "test_1": [
                {
                    "question": "Two software developers disagree on whether to use a JavaScript framework or a native approach for building a web application.",
                    "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict",
                                "Structural Conflict", "Value-Based Conflict"],
                    "right_choices": 0
                }
            ],
            "test_2": [
                {
                    "question": "An engineer faces a dilemma between taking a lucrative job offer in a high-tech industry or continuing to work on a startup with a passion for renewable energy.",
                    "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict",
                                "Structural Conflict", "Value-Based Conflict"],
                    "right_choices": 1
                }
            ],
            "test_3": [
                {
                    "question": "A university's engineering department is reorganized, leading to confusion about new roles and responsibilities within the team.",
                    "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict",
                                "Structural Conflict", "Value-Based Conflict"],
                    "right_choices": 3
                }
            ],
            "test_4": [
                {
                    "question": "A team of researchers with different cultural backgrounds struggles to agree on how to design their experiment.",
                    "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict",
                                "Structural Conflict", "Value-Based Conflict"],
                    "right_choices": 4
                }
            ],
            "test_5": [
                {
                    "question": "A project manager needs to decide whether to prioritize a technical feature or focus on user experience for an upcoming product launch.",
                    "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict",
                                "Structural Conflict", "Value-Based Conflict"],
                    "right_choices": 1
                }
            ],
            "test_6": [
                {
                    "question": "Two team members in a robotics club argue over the allocation of project resources, each believing their approach is more efficient.",
                    "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict",
                                "Structural Conflict", "Value-Based Conflict"],
                    "right_choices": 0
                }
            ],
            "test_7": [
                {
                    "question": "A large tech company faces disagreements among top-level executives about the company's future direction, especially regarding artificial intelligence versus traditional computing.",
                    "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict",
                                "Structural Conflict", "Value-Based Conflict"],
                    "right_choices": 2
                }
            ]
        })

# @routes.route('/get_courses', methods=['POST'])
# def get_courses():
#     username = request.json.get('username')
#
#     if not username:
#         return jsonify({'message': 'Username required!'}), 400
#
#     connection = get_db_connection()
#
#     if not connection:
#         return jsonify({'message': 'Database connection failed'}), 503
#
#     try:
#         table_name = 'users_info'
#         cursor.execute(f'SELECT * FROM {table_name} WHERE user_name = ?', (username,))
#         id = cursor.fetchone()[0]
#
#         table_name = 'users_courses'
#         cursor.execute(f'SELECT * FROM {table_name} WHERE user_id = ?', (id,))
#         courses = cursor.fetchall()
#     except mariadb.Error as e:
#         print(f"Error querying database: {e}")
#         courses = None
#     finally:
#         cursor.close()
#         connection.close()
#
#     if courses:
#         return jsonify({'message': 'There are some courses', 'courses': courses}), 200
#     return jsonify({'message': 'No registered courses!'}), 401
#
# @routes.route('/get_theor_and_actv_count', methods=['POST'])
# def get_theor_and_actv_count():
#     course = request.json.get('course')
#
#     if not course:
#         return jsonify({'message': 'Name of the course required!'}), 400
#
#     connection = get_db_connection()
#
#     if not connection:
#         return jsonify({'message': 'Database connection failed'}), 503
#
#     try:
#         table_name = 'courses'
#         cursor.execute(f'SELECT * FROM {table_name} WHERE course_name = ?', (username,))
#         course_id = cursor.fetchone()
#
#         table_name = 'study_plan'
#         cursor.execute(f'SELECT * FROM {table_name} WHERE course_id = ?', (course_id,))
#         sp_id = cursor.fetchone()
#
#         table_name = 'activities'
#         cursor.execute(f'SELECT * FROM {table_name} WHERE sp_id = ?', (sp_id,))
#         sp_id = cursor.fetchone()
#     except mariadb.Error as e:
#         print(f"Error querying database: {e}")
#         courses = None
#     finally:
#         cursor.close()
#         connection.close()

# @routes.route('/<path:path>', methods=['GET'])
# def static(path):
#     return send_from_directory('../frontend/public', path)
#
# @routes.route('/shit', methods=['POST'])
# def shit():
#     return jsonify("Fuck you")
#
# @routes.route('/')
# @routes.route('/login', methods=['GET'])
# def login():
#     # username = request.json.get('username')
#     # password = request.json.get('password')
#     #
#     # user = User.query.filter_by(username=username).first()
#     # if user and bcrypt.check_password_hash(user.password, password):
#     #     access_token = create_access_token(identity={'id': user.id, 'username': user.username})
#     #     return jsonify({'access_token': access_token}), 200
#     #
#     # return jsonify({'message': 'Invalid credentials'}), 401
#     return redirect('/index.html')
#
#
# @routes.route('/courses', methods=['GET'])
# @jwt_required()
# def get_courses():
#     courses = Course.query.all()
#     return courses_schema.jsonify(courses), 200
#
# @routes.route('/courses', methods=['POST'])
# @jwt_required()
# def add_course():
#     title = request.json.get('title')
#     description = request.json.get('description')
#
#     if not title or not description:
#         return jsonify({'message': 'Title and description are required'}), 400
#
#     new_course = Course(title=title, description=description)
#     db.session.add(new_course)
#     db.session.commit()
#
#     return course_schema.jsonify(new_course), 201
