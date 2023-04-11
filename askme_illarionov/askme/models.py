from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def is_correct(self, question_id):
        if question_id > len(self.all()) or question_id < 0:
            return False
        return True

    def get_new_questions(self):
        return self.order_by('-posted_time')

    def get_question_and_answers(self, question_id):
        question = self.get(id__exact=question_id)
        return tuple([question, question.answer_set.all()])

    def get_hot(self):
        return self.order_by('-likes')


class Question(models.Model):
    tags = models.ManyToManyField('Tag', blank=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    STATUS_CHOICES = [
        ('d', 'discussing'),
        ('c', 'closed')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    posted_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True)

    objects = QuestionManager()

    def __str__(self):
        # res = ""
        # for tag in self.tags:
        #     res = res + str(tag) + " "
        return self.title


class AnswerManager(models.Manager):
    pass


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    text = models.TextField()
    STATUS_CHOICES = [
        ('c', 'correct'),
        ('u', 'uncorrect')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    posted_time = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True)

    objects = AnswerManager()


class TagManager(models.Manager):
    def get_questions_by_tag(self, tag):
        tags = self.get(name__exact=tag)
        return tags.question_set.all()


class Tag(models.Model):
    name = models.CharField(max_length=255)

    objects = TagManager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    avatar = models.ImageField()


class Like(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, null=True)
