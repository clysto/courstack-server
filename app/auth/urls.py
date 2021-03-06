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
        "/teacher_signup",
        views.teacher_signup,
        methods=[
            "POST",
        ],
    ),
    Route(
        "/student_signup",
        views.student_signup,
        methods=[
            "POST",
        ],
    ),
    Route("/current_user", views.get_current_user),
    Route("/users", views.get_all_users),
]
