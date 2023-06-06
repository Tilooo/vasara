#tot/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'tot'

urlpatterns = [
    path('', views.set_list, name='set_list'),
    path('set/create/', views.create_set, name='create_set'),
    path('set/<int:set_id>/box/create/', views.create_box, name='create_box'),
    path('box/<int:box_id>/flashcard/create/', views.create_flashcard, name='create_flashcard'),
    path('box/<int:box_id>/', views.box_detail, name='box_detail'),
    path('flashcard/<int:flashcard_id>/edit/', views.edit_flashcard, name='edit_flashcard'),
    path('flashcard/<int:flashcard_id>/delete/', views.delete_flashcard, name='delete_flashcard'),
    path('flashcard/<int:flashcard_id>/', views.flashcard_detail, name='flashcard_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]




