from django.urls import path
from . import views


urlpatterns = [
    path('test', views.searchTest, name='searchTest'),
    #path('test', views.cacheTest, name='searchTest'),
    path('getPage', views.getPage, name='getPage'),
    path('send', views.sendQuery, name='send'),
    path('getStatistics', views.getStatistics, name='getStatistics'),
    path('sendFilters', views.sendFilters, name='sendFilters')
]