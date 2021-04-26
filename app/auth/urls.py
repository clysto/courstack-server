from starlette.routing import Route

from . import views

routes = [
    Route(
        "/login",
        views.login,
        methods=[
            "POST",
        ],
    ),
    Route(
        "/signup",
        views.teacher_signup,
        methods=[
            "POST",
        ],
    ),
    Route("/current_user", views.get_current_user),
]
