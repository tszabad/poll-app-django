from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('addpoll/', views.addpoll, name='addpoll'),
    path('edit/<int:question_id>/', views.edit_question, name='edit_question'),
    path('edit_choice/<int:choice_id>/', views.edit_choice, name='edit_answer'),
    path('<int:question_id>/addanswer/', views.addanswer, name='addanswer'),
    path('delete/choice/<int:choice_id>/', views.delete_choice, name='choice_confirm_delete'),
    path('delete/question/<int:question_id>/', views.delete_question, name='question_confirm_delete'),
    path('resultdata/<str:obj>/', views.resultdata, name='resultdata'),
   
    
]