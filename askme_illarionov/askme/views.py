from django.shortcuts import render
from . import models
from django.http import HttpResponse, HttpResponseBadRequest


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context)


def question(request, question_id):
    if question_id >= len(models.QUESTIONS):
        return HttpResponseBadRequest
    answers = []
    for answer in models.ANSWERS:
        if answer['question_id'] == question_id:
            answers.append(answer)
    context = {'question': models.QUESTIONS[question_id], 'answers': answers}
    return render(request, 'question.html', context)


def ask(request):
    return render(request, 'new_question.html')


def settings(request):
    return render(request, 'settings.html')


def hot(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'hot.html', context)


def tag(request, *args, **kwargs):
    question_tag = kwargs['tag']
    questions = []
    for question_by_tag in models.QUESTIONS:
        if question_tag in question_by_tag.get('tags'):
            questions.append(question_by_tag)
    if not questions:
        return HttpResponseBadRequest()
    context = {'questions': questions, 'tag': question_tag}
    return render(request, 'tag.html', context)


def signup(request):
    return render(request, 'registration.html')


def login(request):
    return render(request, 'login.html')
