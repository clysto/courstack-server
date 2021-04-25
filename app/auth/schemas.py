from marshmallow import Schema, fields, post_load

from .models import Teacher


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    fullname = fields.String(required=True)
    user_type = fields.String(dump_only=True)


class TeacherSchema(UserSchema):
    @post_load
    def create_teacher(self, item, many, **kwargs):
        return Teacher(**item)


user_schema = UserSchema()
teacher_schema = TeacherSchema()
