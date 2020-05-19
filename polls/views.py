from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView
from django.utils import timezone

from .models import Choice, Question
from .forms import PollForm, PollAnswerForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
        pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)   
    return render(request, 'polls/results.html', {'question': question} )

def addpoll(request):
        
        form = PollForm(request.GET)
        if request.method == "POST":
        # create a form instance and populate it with data from the request:
            form = PollForm(request.POST or None)
        # check whether it's valid:
        if form.is_valid():
            Question.objects.create(**form.cleaned_data)
            return redirect("../")
            

        return render(request, 'polls/addpoll.html', {'form': form})

def addanswer(request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = PollAnswerForm(request.GET)
        if request.method == "POST":
        # create a form instance and populate it with data from the request:
            form = PollAnswerForm(request.POST or None)
        # check whether it's valid:
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.question = question
            new_choice.save()
            return redirect("../")
            

        return render(request, 'polls/addanswer.html', {'form': form, 'question':question})
        
        
def resultdata(request, obj):
    question = Question.objects.get(id=obj)
    choice_data = question.choice_set.all()
   
    data = []
    for choice in choice_data:
        data.append({choice.choice_text : choice.votes})
    return JsonResponse(data, safe=False)