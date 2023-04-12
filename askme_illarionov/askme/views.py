from django.shortcuts import render
from . import models
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator


def paginate(object_list, request, html, per_page=5, context=dict()):
    paginator = Paginator(object_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request, html, context)


def index(request):
    new_questions = models.Question.objects.get_new_questions()
    return paginate(new_questions, request, 'index.html', 5)


def question(request, question_id):
    if not models.Question.objects.is_correct(question_id):
        return HttpResponseBadRequest()
    tmp_question, answers = models.Question.objects.get_question_and_answers(question_id)
    context = {'question': tmp_question[0], 'num_likes': tmp_question[1], 'num_answers': tmp_question[2]}
    return paginate(answers, request, 'question.html', 3, context)


def ask(request):
    return render(request, 'new_question.html')


def settings(request):
    return render(request, 'settings.html')


def hot(request):
    hot_questions = models.Question.objects.get_hot()
    return paginate(hot_questions, request, 'hot.html', 5)


def tag(request, *args, **kwargs):
    question_tag = kwargs['tag']
    questions = models.Tag.objects.get_questions_by_tag(question_tag)
    context = {'tag': question_tag}
    return paginate(questions, request, 'tag.html', 5, context)


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
