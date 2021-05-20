from marshmallow import Schema, fields, post_load

from app.auth.schemas import TeacherSchema

from .models import Attachment, Course, CourseSection, SignInTask


class CourseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    teacher = fields.Nested(TeacherSchema, dump_only=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    cover = fields.String()

    @post_load
    def create_course(self, item, many, **kwargs):
        return Course(**item)


class AttachmentSchema(Schema):
    id = fields.Integer(dump_only=True)
    original_filename = fields.String(required=True)
    filename = fields.String(required=True)

    @post_load
    def create_attachment(self, item, many, **kwargs):
        return Attachment(**item)


class CourseSectionSchema(Schema):
    id = fields.Integer(dump_only=True)
    course_id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    content = fields.String(required=True)
    date = fields.Date(required=True)
    attachments = fields.List(fields.Nested(AttachmentSchema), required=True)

    @post_load
    def create_course_section(self, item, many, **kwargs):
        return CourseSection(**item)


class SignInTaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    time_start = fields.DateTime(required=True)
    time_end = fields.DateTime(required=True)
    course_id = fields.Integer()

    @post_load
    def create_sign_in_task(self, item, many, **kwargs):
        return SignInTask(**item)


course_schema = CourseSchema()
course_section_schema = CourseSectionSchema()
sign_in_task_schema = SignInTaskSchema()
