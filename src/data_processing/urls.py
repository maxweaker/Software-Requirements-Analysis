from django.urls import path
from . import views


urlpatterns = [
    path('read_data', views.read_data, name='read_data'),
    path('clean_data', views.clean_data, name='clean_data'),
    path('build_index', views.build_index, name='build_index'),
    path('test', views.test, name='test'),
    path('import_doc', views.import_doc, name='import_doc'),

]