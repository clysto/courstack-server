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


class PasswordIncorrectException(APIException):
    status_code = 401
    detail = "用户密码错误"


class UnauthorizedException(APIException):
    status_code = 401
    detail = "未认证的用户"
