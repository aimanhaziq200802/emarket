from django.urls import path
from . import views

app_name = 'uploadcsv'

urlpatterns = [
    path('upload_csv/', views.upload_csv, name='upload_csv'),
]