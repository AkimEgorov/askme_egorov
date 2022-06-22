from random import randint

from django.core.management.base import BaseCommand
from faker import Faker

from app.models import *

COUNT_TAG = 10010
COUNT_USER = 10010
COUNT_QUESTION = 100010
COUNT_TAG_IN_QUESTION = 5
COUNT_ANSWER = 1000010
COUNT_LIKE_QUESTION = 1000
COUNT_LIKE_ANSWER = 1000


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        tags = [
            Tag(
                title=faker.word() + str(i)
            )
            for i in range(COUNT_TAG)
        ]
        Tag.objects.bulk_create(tags)

        user = []
        for i in range(COUNT_USER):
            user.append(User(
                id=i,
                username=faker.simple_profile()['username'] + str(i),
                email=faker.email(),
                password=faker.password()
            ))
            print(i)
        User.objects.bulk_create(user)

        profile = []
        for i in range(COUNT_USER):
            profile.append(Profile(
                user=User.objects.get(pk=i),
                #nickname=faker.simple_profile()['username'] + str(i)
            ))
            print('p', i)
        Profile.objects.bulk_create(profile)

        for i in range(COUNT_QUESTION):
            question = Question.objects.create(
                author=User.objects.get(pk=randint(0,COUNT_USER-1)),
                title="Question"+str(i),
                content=faker.text
            )
            tags = []
            for j in range(COUNT_TAG_IN_QUESTION):
                tags.append(Tag.objects.get(pk=randint(Tag.objects.first().id, Tag.objects.last().id)))
            question.tags.add(*tags)
            print(i)

        answer = []
        for i in range(COUNT_ANSWER):
            print(i)
            answer.append(Answer(
                content=faker.text,
                author=User.objects.get(pk=randint(0, COUNT_USER-1)),
                question=Question.objects.get(pk=randint(Question.objects.first().id, Question.objects.last().id)),
                user_rating=randint(-100, 100),
            ))
        Answer.objects.bulk_create(answer)
