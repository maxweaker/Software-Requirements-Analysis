from django.urls import path, re_path
from .views import *
app_name = 'Home'

urlpatterns = [
    path("hotPapers/", HotPapers.as_view()),
]
