from starlette.routing import Route

from . import views

routes = [
    Route("/courses", views.get_all_courses),
    Route("/courses", views.create_course, methods=["POST"]),
    Route("/courses/{course_id:int}/sections", views.get_course_sections),
    Route(
        "/courses/{course_id:int}/sign_in_tasks",
        views.create_sign_in_task,
        methods=["POST"],
    ),
    Route("/courses/{course_id:int}/sign_in_tasks", views.get_sign_in_task),
    Route(
        "/courses/{course_id:int}/sections",
        views.create_course_section,
        methods=["POST"],
    ),
    Route(
        "/sign_in_tasks/{sign_in_task_id:int}/sign_in",
        views.course_sign_in,
        methods=["POST"],
    ),
    Route("/files", views.upload_file, methods=["POST"]),
    Route("/files/{file_id:uuid}", views.download_file),
]
