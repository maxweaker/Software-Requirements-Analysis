from django.urls import path
from . import views


urlpatterns = [
    path('read_data', views.read_data, name='read_data'),
]