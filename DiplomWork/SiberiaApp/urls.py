from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path('giveInfoTest/ajax/', views.giveInfoTest),
    path('giveInfo/ajax/', views.giveInfo),
    path('cybercode/ajax/', views.cybercode),
    path('search/ajax/', views.search),
    path('allpeople/ajax/', views.allpeople),
    path('needHistory/ajax/', views.needHistory),
    path('needHistoryMarker/ajax/', views.needHistoryMarker),
    path('counterPeopleOnMarker/ajax/', views.counterPeopleOnMarker),
    path('peopleOnMarker/ajax/', views.peopleOnMarker),
    path('', login_required(views.indexRework)),
]
