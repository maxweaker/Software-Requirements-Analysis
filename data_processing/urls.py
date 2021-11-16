from django.urls import path
from . import views


urlpatterns = [
    path('read_data', views.read_data, name='read_data'),
    path('clear_data', views.clear_data, name='clear_data'),
    path('clean_data', views.clean_data, name='clean_data'),
]