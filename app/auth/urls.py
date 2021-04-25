from starlette.routing import Route

from . import views

routes = [Route("/login", views.teacher_login), Route("/signup", views.teacher_signup)]
