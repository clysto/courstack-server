from starlette.responses import JSONResponse


def root(request):
    return JSONResponse(
        {"title": "courstack server", "version": "0.1", "author": "毛亚琛"}
    )


def http_exception(request, exc):
    return JSONResponse(
        {"status_code": exc.status_code, "detail": exc.detail},
        status_code=exc.status_code,
    )


def body_validation_exception(request, exc):
    return JSONResponse(
        {"status_code": exc.status_code, "detail": exc.detail, "errors": exc.errors},
        status_code=exc.status_code,
    )


def api_exception(request, exc):
    return JSONResponse(
        {"status_code": exc.status_code, "detail": exc.detail},
        status_code=exc.status_code,
    )
