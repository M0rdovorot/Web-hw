import django.db.models
from django.db import models
from django.contrib.auth.models import User, AbstractUser


def get_question_info(questions):
    questions_and_info = []
    for question in questions:
        questions_and_info.append(tuple([question, question.answer_set.all().count]))
    return questions_and_info


# def get_answer_info(answers):
#     answers_and_info = []
#     for answer in answers:
#         answers_and_info.append(answer)
#     return answers_and_info


class QuestionManager(models.Manager):

    def is_correct(self, question_id):
        if self.filter(id__exact=question_id).exists():
            return False
        return True

    def get_new_questions(self):
        questions = self.order_by('-posted_time')
        return get_question_info(questions)

    def get_question_and_answers(self, question_id):
        question = self.get(id__exact=question_id)
        question = get_question_info([question])[0]
        answers = question[0].answer_set.all()
        return tuple([question, answers])

    def get_hot(self):
        questions = self.alias(num_likes=django.db.models.Count('likequestion')).order_by('-num_likes')
        return get_question_info(questions)

    # def get_question_likes(self, question_id):
    #     return self.get(id__exact=question_id).likequestion_set.all().count()


class Question(models.Model):
    tags = models.ManyToManyField('Tag', blank=True, default=None)
    title = models.CharField(max_length=255)
    text = models.TextField()
    STATUS_CHOICES = [
        ('d', 'discussing'),
        ('c', 'closed')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    posted_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(default=0)
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
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='u')
    posted_time = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(default=0)

    objects = AnswerManager()


class TagManager(models.Manager):
    def get_questions_by_tag(self, tag):
        tags = self.get(name__exact=tag)
        questions = tags.question_set.all()
        return get_question_info(questions)



class Tag(models.Model):
    name = models.CharField(max_length=255)

    objects = TagManager()

    def __str__(self):
        return self.name


class Profile(AbstractUser):
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars/%Y/%m/%d/', default="DefaultAvatar.jpeg")


# class Like(models.Model):
#     user = models.ForeignKey('Profile', on_delete=models.CASCADE)
#     question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
#     answer = models.ForeignKey('Answer', on_delete=models.CASCADE, null=True)


class LikeQuestion(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)


class LikeAnswer(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
