from starlette.exceptions import HTTPException


class APIException(HTTPException):
    status_code = 400
    detail = "API错误"

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail


class BodyValidationException(HTTPException):
    status_code = 400
    detail = "Body验证错误"

    def __init__(self, exc):
        self.data = exc.data
        self.errors = exc.messages


class UserExistException(APIException):
    detail = "该用户已存在"


class UserNotExistException(APIException):
    status_code = 404
    detail = "该用户不存在"


class CourseNotFoundException(APIException):
    status_code = 404
    detail = "该课程不存在"

    def __init__(self, course_id=None):
        if course_id is not None:
            self.detail = "课程%d不存在" % course_id


class SignInTaskNotFoundException(APIException):
    status_code = 404
    detail = "该签到任务不存在"

    def __init__(self, sign_in_task_id=None):
        if sign_in_task_id is not None:
            self.detail = "签到任务%d不存在" % sign_in_task_id


class SignInTaskExpiredException(APIException):
    detail = "该签到任务已过期"


class NotCourseOwnerException(APIException):
    detail = "您不是该课程的创建者"


class PasswordIncorrectException(APIException):
    status_code = 401
    detail = "用户密码错误"


class UnauthorizedException(APIException):
    status_code = 401
    detail = "未认证的用户"
