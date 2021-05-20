from starlette.routing import Route

from . import views

routes = [
    Route("/courses", views.get_all_courses),
    Route("/courses/{course_id:int}", views.get_course_detail),
    Route("/courses/{course_id:int}/rtc_token", views.get_rtc_token),
    Route("/courses", views.create_course, methods=["POST"]),
    Route("/courses/{course_id:int}/sections", views.get_course_sections),
    Route(
        "/course_sections/{course_section_id:int}",
        views.delete_course_section,
        methods=["DELETE"],
    ),
    Route(
        "/courses/{course_id:int}/sign_in_tasks",
        views.create_sign_in_task,
        methods=["POST"],
    ),
    Route("/courses/{course_id:int}/sign_in_tasks", views.get_sign_in_task),
    Route("/courses/{course_id:int}/select", views.select_course, methods=["POST"]),
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
    Route(
        "/sign_in_tasks/{sign_in_task_id:int}/students",
        views.get_sign_in_students,
    ),
    Route(
        "/rooms/{room_name_prefix}",
        views.get_active_rooms,
    ),
    Route("/files", views.upload_file, methods=["POST"]),
    Route("/download/{filename}", views.download_file),
    Route("/students/courses", views.get_student_courses),
    Route("/courses/{course_id:int}/students", views.get_course_students),
]
