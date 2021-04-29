from marshmallow import Schema, fields, post_load

from app.auth.schemas import TeacherSchema

from .models import Course, CourseSection


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


class CourseSectionSchema(Schema):
    id = fields.Integer(dump_only=True)
    course_id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    content = fields.String(required=True)
    date = fields.Date(required=True)
    attachments = fields.List(fields.UUID, required=True)

    @post_load
    def create_course_section(self, item, many, **kwargs):
        return CourseSection(**item)


class FileSchema(Schema):
    id = fields.UUID()
    filename = fields.String()


course_schema = CourseSchema()
course_section_schema = CourseSectionSchema()
file_schema = FileSchema()
