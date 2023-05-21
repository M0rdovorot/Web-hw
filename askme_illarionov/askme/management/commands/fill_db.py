from django.core.management.base import BaseCommand, CommandError
from askme import models


class Command(BaseCommand):
    help = "Fill the database with content"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **options):
        ratio = options["ratio"]
        profiles = []
        tags = []
        users = []
        questions = []
        answers = []
        likes = []
        new_row_id = models.Profile.objects.all().count() + 1
        # for i in range(new_row_id, ratio + new_row_id):
        #     user = models.User.objects.create_user(id=i, username=f'User {i}', email=None, password=None)
        #     users.append(user)

        for i in range(new_row_id, ratio + new_row_id):
            profile = models.Profile.objects.create_user(id=i, username=f'User {i}', password=f'12345', avatar=None)
            profile.save()
            profiles.append(profile)
        # models.Profile.objects.bulk_create(profiles)

        tag_new_row_id = models.Profile.objects.all().count() + 1
        for i in range(tag_new_row_id, ratio + tag_new_row_id):
            tag = models.Tag(id=i, name=f'{i}')
            tags.append(tag)
        new_row_id = models.Question.objects.all().count() + 1
        for i in range(new_row_id, ratio * 10 + new_row_id):
            question = models.Question(id=i, title=f'title {i}', text=f'text {i}', status='d', profile=profiles[(i - new_row_id) % ratio])
            questions.append(question)
        models.Question.objects.bulk_create(questions)
        models.Tag.objects.bulk_create(tags)

        for i in tags:
            for j in questions:
                i.question_set.add(j)

        new_row_id = models.Answer.objects.all().count() + 1
        for i in range(new_row_id, new_row_id + ratio * 100):
            answer = models.Answer(id=i, question=questions[(i-new_row_id) % (ratio * 10)], text=f'text {i}', status='c', profile=profiles[(i - new_row_id) % ratio])
            answers.append(answer)
        models.Answer.objects.bulk_create(answers)

        new_row_id = models.Like.objects.all().count() + 1
        for i in range(new_row_id, + new_row_id + ratio * 200):
            like = models.Like(id=i, user=profiles[(i-new_row_id) % ratio], question=questions[(i - new_row_id) % (ratio * 10)], answer=None)
            likes.append(like)
        models.Like.objects.bulk_create(likes)
        return
