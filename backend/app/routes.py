from flask import Blueprint, jsonify, request, send_from_directory
# from .models import User, Course
# from .schemas import user_schema, course_schema, courses_schema
# from . import db, bcrypt

routes = Blueprint('routes', __name__)


# @routes.route('/register', methods=['POST'])
# def register():
#     username = request.json.get('username')
#     password = request.json.get('password')
#
#     if not username or not password:
#         return jsonify({'message': 'Username and password are required'}), 400
#
#     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#     new_user = User(username=username, password=hashed_password)
#     db.session.add(new_user)
#     db.session.commit()
#
#     return user_schema.jsonify(new_user), 201


# @routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')
#
#     user = User.query.filter_by(username=username).first()
#     if user and bcrypt.check_password_hash(user.password, password):
#         access_token = create_access_token(identity={'id': user.id, 'username': user.username})
#         return jsonify({'access_token': access_token}), 200
#
#     return jsonify({'message': 'Invalid credentials'}), 401


# @routes.route('/courses', methods=['GET'])
# # @jwt_required()
# def get_courses():
#     courses = Course.query.all()
#     return courses_schema.jsonify(courses), 200

@routes.route('/<path:path>')
def static_file(path):
    return send_from_directory('../../frontend/public', path)


@routes.route('/study_plan')
def get_study_plan():
    return jsonify({
        "study_plan": [
        { "day_number": 1, "topic": "Understanding Conflict", "available": True },
        { "day_number": 2, "topic": "Conflict Causes and Triggers", "available": False },
        { "day_number": 3, "topic": "Conflict Response Styles", "available": False },
        { "day_number": 4, "topic": "Active Listening", "available": False },
        { "day_number": 5, "topic": "Non-Verbal Communication", "available": False },
        { "day_number": 6, "topic": "Assertive Communication", "available": False },
        { "day_number": 7, "topic": "Emotional Regulation", "available": False },
        { "day_number": 8, "topic": "Negotiation Fundamentals", "available": False },
        { "day_number": 9, "topic": "Conflict Resolution Strategies", "available": False }
    ]})


@routes.route('/day_plan', methods=['POST'])
def get_day_plan():
    day = request.json.get('day_number')
    return jsonify(
        {'message': 'smth','activities_number': 3})


@routes.route('/theory', methods=['POST'])
def get_theory():
    day = request.json.get('day_number')
    print(day)
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


@routes.route('/activity', methods=['POST'])
def get_activity():
    day = request.json.get('day_number')
    print('activity', day)
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
