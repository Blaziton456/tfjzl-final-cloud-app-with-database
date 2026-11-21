
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Course, Enrollment, Submission, Choice


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    choices = extract_answers(request)

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    valid_choices = Choice.objects.filter(
        id__in=choices,
        question__course=course
    )

    submission.choices.set(valid_choices)

    return HttpResponseRedirect(
        reverse(
            'show_exam_result',
            args=(course_id, submission.id)
        )
    )


def extract_answers(request):
    submitted_answers = []

    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]

            try:
                choice_id = int(value)
                submitted_answers.append(choice_id)
            except (ValueError, TypeError):
                continue

    return submitted_answers



def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        enrollment__course=course,
        enrollment__user=request.user
    )

    selected_choices = submission.choices.all()

    questions = course.question_set.all().prefetch_related(
        'choice_set'
    )

    total_score = 0
    correct_answers = 0
    question_results = []

    for question in questions:
        question_choices = selected_choices.filter(
            question=question
        )

        selected_ids = list(
            question_choices.values_list('id', flat=True)
        )

        is_correct = question.is_get_score(selected_ids)

        if is_correct:
            total_score += question.grade
            correct_answers += 1

        question_results.append({
            'question': question,
            'choices': question.choice_set.all(),
            'selected_choices': question_choices,
            'is_correct': is_correct,
            'grade': question.grade,
        })

    context = {
        'course': course,
        'submission': submission,
        'grade': total_score,
        'total_score': total_score,
        'correct_answers': correct_answers,
        'total_questions': len(question_results),
        'choices': selected_choices,
        'questions': questions,
        'question_results': question_results,
    }

    return render(
        request,
        'onlinecourseapp/exam_result.html',
        context
    )
