from marshmallow import Schema, fields, post_load

from .models import Teacher, Student


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    fullname = fields.String(required=True)
    user_type = fields.String(dump_only=True)


class TeacherSchema(UserSchema):
    @post_load
    def create_teacher(self, item, many, **kwargs):
        return Teacher(**item)


class StudentSchema(UserSchema):
    @post_load
    def create_student(self, item, many, **kwargs):
        return Student(**item)


user_schema = UserSchema()
teacher_schema = TeacherSchema()
student_schema = StudentSchema()
