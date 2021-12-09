from django.urls import path
from . import views


urlpatterns = [
    path('test', views.searchTest, name='searchTest'),
    #path('test', views.cacheTest, name='searchTest')
]