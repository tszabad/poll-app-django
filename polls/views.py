import datetime

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Choice, Question
from .forms import PollForm, PollAnswerForm, EditQuestionForm


class IndexView(generic.ListView):
    paginate_by = 5
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        
        """Return the last five published questions."""
        return Question.objects.filter(
        pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:10]



class DetailView(generic.DetailView):
    
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
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

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)   
    return render(request, 'polls/results.html', {'question': question} )

@login_required
def addpoll(request):
        
        form = PollForm(request.GET)
        if request.method == "POST":
        # create a form instance and populate it with data from the request:
            form = PollForm(request.POST or None)
        # check whether it's valid:
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.pub_date = datetime.datetime.now()
            new_poll.owner = request.user
            new_poll.save()
            return redirect("../")
            

        return render(request, 'polls/addpoll.html', {'form': form})

@login_required
def addanswer(request, question_id):
        question = get_object_or_404(Question, id=question_id)
        if request.user != question.owner:
           return redirect('/')
        form = PollAnswerForm(request.GET)
        if request.method == "POST":
        # create a form instance and populate it with data from the request:
            form = PollAnswerForm(request.POST or None)
        # check whether it's valid:
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.question = question
            new_choice.save()
            messages.success(
                            request,
                            'Choice added!',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect("../")
            

        return render(request, 'polls/addanswer.html', {'form': form, 'question':question})
        
@login_required        
def resultdata(request, obj):
    question = Question.objects.get(id=obj)
    choice_data = question.choice_set.all()
   
    data = []
    for choice in choice_data:
        data.append({choice.choice_text : choice.votes})
    return JsonResponse(data, safe=False)


 
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user != question.owner:
        return redirect('/')

    if request.method == "POST":
        form = EditQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(
                            request,
                            'Question Edit Successfully',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
        return redirect('/polls')
    else:
        form = EditQuestionForm(instance=question)

    return render(request, 'polls/edit_question.html', {'form': form, 'question':question})

def edit_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    question = get_object_or_404(Question, id=choice.question_id)
    if request.user != question.owner:
        return redirect('/')

    if request.method == "POST":
        form = PollAnswerForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            
            messages.success(
                            request,
                            'Question Edit Successfully',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
        return redirect('/polls')
    else:
        form = PollAnswerForm(instance=choice)

    return render(request, 'polls/addanswer.html', {'form':form, 'choice':choice})

@login_required
def delete_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    question = get_object_or_404(Question, id=choice.question_id)
    if request.user != question.owner:
        return redirect('/')

    if request.method == "POST":
        choice.delete()
        messages.success(
                        request,
                        'Choice Deleted Successfully',
                        extra_tags='alert alert-success alert-dismissible fade show'
                        )
        return redirect('/polls')

    return render(request, 'polls/delete_choice_confirm.html', {'choice':choice})


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user != question.owner:
        return redirect('/')

    if request.method == "POST":
        question.delete()
        messages.success(
                        request,
                        'Poll Deleted Successfully',
                        extra_tags='alert alert-success alert-dismissible fade show'
                        )
        return redirect('/polls')

    return render(request, 'polls/delete_question_confirm.html', {'question':question})