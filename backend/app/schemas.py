from . import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username')

class CourseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

user_schema = UserSchema()
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)