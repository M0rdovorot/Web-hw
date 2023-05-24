import time
from uuid import uuid4

from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST

from . import models
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse, resolve
import jwt

from .forms import LoginForm, RegistrationForm, SettingsForm, AskForm, AnswerForm
import os

from .models import Profile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "askme_illarionov.askme_illarionov.settings")


def paginate(object_list, request, html, per_page=5, context=dict(), is_last=False):
    paginator = Paginator(object_list, per_page)
    if is_last:
        page_number = int(len(object_list) / per_page) + 1
    else:
        page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request, html, context)


@login_required(login_url='login/', redirect_field_name="continue")
def index(request):
    new_questions = models.Question.objects.get_new_questions()
    context = {'user': request.user}
        # , 'top_tags': models.Tag.objects.get_popular_tags(), 'top_users': models.Profile.object.get_active_users()}
    return paginate(new_questions, request, 'index.html', 5, context)


from cent import Client, CentException

client = Client("http://localhost:8003/api", api_key="my_api_key", timeout=1)


def question(request, question_id):
    # if not models.Question.objects.is_correct(question_id):
    #     return HttpResponseBadRequest()
    try:
        models.Question.objects.get(id__exact=question_id)
    except models.Question.DoesNotExist:
        return HttpResponseBadRequest("No such question")

    chan_id = f'question_{question_id}' #new

    tmp_question, answers = models.Question.objects.get_question_and_answers(question_id)
    if request.method == 'GET':
        answer_form = AnswerForm()
    elif request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            a = answer_form.save(request.user, tmp_question[0])
            a.save()

            client.publish(chan_id, model_to_dict(a)) #new

            tmp_question, answers = models.Question.objects.get_question_and_answers(question_id)
            context = {'question': tmp_question[0], 'num_answers': tmp_question[1]}
            context['form'] = answer_form
            return paginate(answers, request, 'question.html', 3, context, True)
        answer_form.add_error(None, 'Answer saving error')
    # sub_id = uuid4()
    context = {'question': tmp_question[0], 'num_answers': tmp_question[1], 'server_address': 'ws://127.0.0.1:8003/connection/websocket',  #new
               'cent_chan': chan_id, 'secret_token': jwt.encode({"sub": str(request.user.pk), "exp": int(time.time()) + 10*60}, "my_secret")}
    context['form'] = answer_form
    return paginate(answers, request, 'question.html', 3, context)


@login_required(login_url='login/', redirect_field_name="continue")
def ask(request):
    if request.method == 'GET':
        ask_form = AskForm()
    elif request.method == 'POST':
        ask_form = AskForm(request.POST)
        if ask_form.is_valid():
            q = ask_form.save(request.user)
            q.save()
            return redirect(reverse('question', kwargs={'question_id': q.id}))
        ask_form.add_error(None, 'Question saving error')
    return render(request, 'new_question.html', context={'form': ask_form})


@login_required(login_url='login/', redirect_field_name="continue")
@require_http_methods(['GET', 'POST'])
def settings(request):
    if request.method == 'GET':
        data = model_to_dict(request.user)
        settings_form = SettingsForm(initial=data)
    elif request.method == 'POST':
        settings_form = SettingsForm(request.POST, files=request.FILES, instance=request.user) #new instance and file
        if settings_form.is_valid():
            user = settings_form.save()
            if user:
                user.save()
                return redirect(reverse('index'))
            settings_form.add_error(None, 'User editing error')
    return render(request, 'settings.html', context={'form': settings_form, 'user': request.user})


def hot(request):
    hot_questions = models.Question.objects.get_hot()
    return paginate(hot_questions, request, 'hot.html', 5)


def tag(request, *args, **kwargs):
    question_tag = kwargs['tag']
    questions = models.Tag.objects.get_questions_by_tag(question_tag)
    context = {'tag': question_tag}
    return paginate(questions, request, 'tag.html', 5, context)


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'GET':
        registration_form = RegistrationForm()
    elif request.method == 'POST':
        registration_form = RegistrationForm(request.POST, files=request.FILES)
        if registration_form.is_valid():
            user = registration_form.save()
            if user:
                user.save()
                return redirect(reverse('index'))
            registration_form.add_error(None, 'User saving error')
    return render(request, 'registration.html', context={'form': registration_form})


@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)
                if request.GET.__contains__('continue') and request.GET.get('continue') != '':
                    return redirect(request.GET.get('continue'))
                else:
                    return redirect(reverse('index'))
            login_form.add_error(None, "Invalid username or password")

    return render(request, 'login.html', context={'form': login_form})


def logout(request):
    auth.logout(request)
    return redirect(reverse("index"))


@login_required(login_url='login/', redirect_field_name="continue")
@require_POST
def question_like(request):
    question_id = request.POST['question_id']
    print(question_id)

    try:
        q = models.Question.objects.get(id=question_id)
    except models.Question.DoesNotExist:
        return HttpResponseBadRequest("No such answer")

    try:
        like = models.LikeQuestion.objects.get(profile=request.user, question_id=question_id)
        like.delete()
        q.rating -= 1
        q.save()
        return JsonResponse({
            'likes': q.rating
        })
    except models.LikeQuestion.DoesNotExist:
        q.rating += 1
        #transaction????
        like = models.LikeQuestion.objects.create(question=q, profile=request.user)#profile???
        like.save()
        q.save()
        print(q.rating)
        return JsonResponse({
            'likes': q.rating
        })


@login_required(login_url='login/', redirect_field_name="continue")
@require_POST
def answer_like(request):
    answer_id = request.POST['answer_id']
    print(answer_id)

    #check id
    try:
        a = models.Answer.objects.get(id=answer_id)
    except models.Answer.DoesNotExist:
        return HttpResponseBadRequest("No such answer")

    try:
        like = models.LikeAnswer.objects.get(profile=request.user, answer_id=answer_id)
        like.delete()
        a.rating -= 1
        a.save()
        return JsonResponse({
            'likes': a.rating
        })
    except models.LikeAnswer.DoesNotExist:
        #transaction????
        a.rating += 1
        like = models.LikeAnswer.objects.create(answer=a, profile=request.user)#profile???
        like.save()
        a.save()
        print(a.rating)
        return JsonResponse({
            'likes': a.rating
        })


@login_required(login_url='login/', redirect_field_name="continue")
@require_POST
def mark_as_correct(request):
    answer_id = request.POST['answer_id']
    print(answer_id)

    #check id
    try:
        a = models.Answer.objects.get(id=answer_id)
    except models.Answer.DoesNotExist:
        return HttpResponseBadRequest("No such answer")

    if a.status == 'c':
        a.status = 'u'
        a.save()
        return JsonResponse({
            'status': a.status
        })
    else:
        #transaction????
        a.status = 'c'
        a.save()
        print(a.status)
        return JsonResponse({
            'status': a.status
        })
