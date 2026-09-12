from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from .models import Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)