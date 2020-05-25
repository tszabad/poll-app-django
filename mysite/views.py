
from django.shortcuts import render
from polls.models import Question


def home (request):
    question = Question.objects.all()
    number = len(question)
    return render(request,  'home.html', {'number': number})

