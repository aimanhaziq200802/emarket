from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('delivery_dashboard/', views.delivery_dashboard, name='delivery_dashboard'),

]