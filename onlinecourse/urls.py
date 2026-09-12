from django.contrib import admin
from django.urls import path
from onlinecourseapp.views import submit, show_exam_result

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submit/', submit, name='submit'),
    path('exam-result/', show_exam_result, name='show_exam_result'),
]