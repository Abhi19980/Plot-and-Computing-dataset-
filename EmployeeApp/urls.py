from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('upload-resume', views.uploadResume,name="upload"),
    path('dataset', views.csvfile,name="dataset"),
    path('dataset/<int:pk>/', views.read_csv,name="dataset/:id/compute"),
    path('dataset/<int:pk>/plot_csv', views.plot_csv,name="dataset/:id/plot_csv"),

    path('Home', index, name='index'),
    path('Data', data, name='data'),
    path('Plot', plot, name='plot'),

]