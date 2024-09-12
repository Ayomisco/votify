from django.urls import path
from . import views

urlpatterns = [
    path('elections/', views.election_list, name='election_list'),
    path('elections/<int:election_id>/vote/',
         views.voting_page, name='voting_page'),
    path('elections/<int:election_id>/vote/<int:candidate_id>/',
         views.vote, name='vote'),
]
