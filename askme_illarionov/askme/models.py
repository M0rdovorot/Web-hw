from django.db import models

QUESTIONS = [
    {
        'tags': [f'{i}', f'{i+1}', 'lol'],
        'id': i,
        'title': f'Question {i}',
        'text': f'Text {i}',
    } for i in range(3)
]

ANSWERS = [
    {
        'id': i,
        'question_id': (i + 2) % 3,
        'text': f'Text {i}'
    } for i in range(7)
]

