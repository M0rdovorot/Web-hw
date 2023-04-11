from django.shortcuts import render
from . import models
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator


def index(request):
    new_questions = models.Question.objects.get_new_questions()
    context = {'questions': new_questions}
    return render(request, 'index.html', context)


def question(request, question_id):
    if not models.Question.objects.is_correct(question_id):
        return HttpResponseBadRequest()
    tmp_question, answers = models.Question.objects.get_question_and_answers(question_id)
    context = {'question': tmp_question, 'answers': answers}
    return render(request, 'question.html', context)


def ask(request):
    return render(request, 'new_question.html')


def settings(request):
    return render(request, 'settings.html')


def hot(request):
    hot_questions = models.Question.objects.get_hot()
    context = {'questions': hot_questions}
    return render(request, 'hot.html', context)


def tag(request, *args, **kwargs):
    question_tag = kwargs['tag']
    questions = models.Tag.objects.get_questions_by_tag(question_tag)
    context = {'questions': questions, 'tag': question_tag}
    return render(request, 'tag.html', context)


def signup(request):
    return render(request, 'registration.html')


def login(request):
    return render(request, 'login.html')


"""
def paginate(request):
    object_list = models..all()
    paginator = Paginator(object_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})
"""
