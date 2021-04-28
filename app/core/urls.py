from starlette.routing import Route

from . import views

routes = [
    Route("/courses", views.get_all_courses),
    Route("/courses", views.create_course, methods=["POST"]),
    Route("/courses/{course_id:int}/sections", views.get_course_sections),
    Route("/files", views.upload_file, methods=["POST"]),
    Route("/files/{file_id:uuid}", views.download_file),
]
