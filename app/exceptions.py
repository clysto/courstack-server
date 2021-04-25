from starlette.exceptions import HTTPException


class APIException(HTTPException):
    status_code = 400
    detail = "API错误"

    def __init__(self, message, detail=None):
        self.message = message
        if detail is None:
            self.detail = detail


class BodyValidationException(HTTPException):
    status_code = 400
    detail = "Body验证错误"

    def __init__(self, exc):
        self.data = exc.data
        self.errors = exc.messages
