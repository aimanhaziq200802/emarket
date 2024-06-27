from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add-location/', views.add_location, name='add_location'),
    path('edit-location/<int:location_id>/', views.edit_location, name='edit_location'),
    path('delete-location/<int:location_id>/', views.delete_location, name='delete_location'),

]