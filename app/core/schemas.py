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


class CourseSectionSchema(Schema):
    id = fields.Integer(dump_only=True)
    course_id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    content = fields.String(required=True)
    date = fields.Date(required=True)
    attachments = fields.Method("get_attachments")

    def get_attachments(self, obj):
        attachments = []
        for attachment_id in obj.attachments:
            attachments.append("http://localhost:8000/core/files/" + attachment_id)
        return attachments


class FileSchema(Schema):
    id = fields.UUID()
    filename = fields.String()


course_schema = CourseSchema()
course_section_schema = CourseSectionSchema()
file_schema = FileSchema()
