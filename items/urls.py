from django.urls import path
from . import views

app_name = "items"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.detail, name="detail"),
    path("browse/", views.browse, name="browse"),
    path('popular/', views.popular_items, name='popular_items'),
    path('new-arrivals/', views.new_arrivals, name='new_arrivals'), 
    path('about/', views.about, name='about'), 

]
