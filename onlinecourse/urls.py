from django.contrib import admin
from django.urls import path
from onlinecourseapp.views import submit, show_exam_result

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:course_id>/submit/', submit, name='submit'),
    path(
        'course/<int:course_id>/submission/<int:submission_id>/result/',
        show_exam_result,
        name='show_exam_result'
    ),
]