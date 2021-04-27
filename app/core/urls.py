from starlette.routing import Route

from . import views

routes = [
    Route("/courses", views.get_all_courses),
    Route("/courses", views.create_course, methods=["POST"]),
]
