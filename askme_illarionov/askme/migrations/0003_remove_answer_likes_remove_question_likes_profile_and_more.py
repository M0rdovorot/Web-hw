# Generated by Django 4.2 on 2023-04-11 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('askme', '0002_question_rename_answers_answer_rename_tags_tag_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='question',
            name='likes',
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('avatar', models.ImageField(upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='askme.answer')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='askme.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='askme.profile')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='askme.profile'),
        ),
        migrations.AddField(
            model_name='question',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='askme.profile'),
        ),
    ]
