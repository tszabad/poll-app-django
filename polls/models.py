import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



class Question(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(editable=False, auto_now_add=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text, self.question.question_text