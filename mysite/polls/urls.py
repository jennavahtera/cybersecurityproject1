from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.AllPollsView.as_view(), name='all_polls'),
    path('my/', views.MyPollsView.as_view(), name='my_polls'),
    path('create/', views.create_question, name='create_question'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]