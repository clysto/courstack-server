from marshmallow import Schema, fields, post_load

from app.auth.schemas import TeacherSchema

from .models import Course


class CourseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    teacher = fields.Nested(TeacherSchema, dump_only=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)

    @post_load
    def create_course(self, item, many, **kwargs):
        return Course(**item)


course_schema = CourseSchema()
