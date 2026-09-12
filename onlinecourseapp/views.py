from django.shortcuts import render, redirect
from .models import Question, Choice, Submission


def submit(request):
    if request.method == 'POST':
        for question in Question.objects.all():
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                Submission.objects.create(
                    question=question,
                    choice=choice
                )

        return redirect('show_exam_result')

    return render(request, 'onlinecourseapp/course_details_bootstrap.html')


def show_exam_result(request):
    submissions = Submission.objects.all()
    total_questions = Question.objects.count()
    correct_answers = submissions.filter(choice__is_correct=True).count()

    return render(
        request,
        'onlinecourseapp/exam_result.html',
        {
            'submissions': submissions,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
        }
    )