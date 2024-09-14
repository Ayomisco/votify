from django.urls import path
from . import views

urlpatterns = [
    path('elections/', views.election_list, name='election_list'),
    path('elections/<int:election_id>/vote/',
         views.voting_page, name='voting_page'),
    path('elections/<int:election_id>/vote/<int:candidate_id>/',
         views.vote, name='vote'),
    path('manifesto/<int:candidate_id>/',
         views.manifesto_view, name='manifesto_view'),
    path('candidates/', views.candidates_list, name='candidates_list'),
    path('candidates-page/', views.candidates_page, name='candidates_page'),

]
