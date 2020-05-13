from django import forms

from.models import Question, Choice

class PollForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_text"]

class PollAnswerForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["choice_text"]