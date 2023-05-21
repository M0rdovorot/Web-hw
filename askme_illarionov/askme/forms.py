from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from . import models
from .models import Profile, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=3)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrong':
            raise ValidationError('Wrong password!')
        return data


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'avatar']

    def clean_password_check(self):
        data = self.cleaned_data['password']
        if data != self.cleaned_data['password_check']:
            raise ValidationError('Password missmatch')
        return

    def save(self):
        self.cleaned_data.pop('password_check')
        return Profile.objects.create_user(**self.cleaned_data)


class SettingsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password_check = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Profile
        fields = ['username', "first_name", 'last_name', 'avatar']

    def save(self, commit=True):
        self.cleaned_data.pop('password_check')
        print(self.cleaned_data)
        user = super().save(commit)

        # user.username = self.cleaned_data['username']
        # user.avatar = self.cleaned_data['avatar']
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password'])
        return user

    def clean_password_check(self):
        data = self.cleaned_data['password']
        if data != self.cleaned_data['password_check']:
            raise ValidationError('Password missmatch')
        return data


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def save(self, user):
        new_row_id = models.Question.objects.all().count() + 1
        question = models.Question.objects.create(text=self.cleaned_data['text'], title=self.cleaned_data['title'], profile=user, status='d')
        for t in self.cleaned_data['tags']:
            tag = models.Tag.objects.get(name__exact=t)
            tag.question_set.add(question)
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def save(self, user, question):
        answer = models.Answer.objects.create(text=self.cleaned_data['text'], profile=user, question=question)
        question.answer_set.add(answer)
        return answer
