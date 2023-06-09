from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from tot.views import flashcard_detail

app_name = 'tot'


urlpatterns = [
    path('', views.home, name='home'),
    path('sets/<int:set_id>/', views.set_detail, name='set_detail'),
    path('sets/', views.set_list, name='set_list'),
    path('set/create/', views.create_set, name='create_set'),
    path('sets/<int:set_id>/box/<int:box_id>/', views.box_detail, name='box_detail'),
    path('set/<int:set_id>/box/create/', views.create_box, name='create_box'),
    path('box/<int:box_id>/flashcard/create/', views.create_flashcard, name='create_flashcard'),
    path('box/<int:box_id>/', views.box_detail, name='box_detail'),
    path('flashcards/<int:flashcard_id>/', views.flashcard_detail, name='flashcard_detail'),
    path('flashcard/<int:flashcard_id>/edit/', views.edit_flashcard, name='edit_flashcard'),
    path('flashcard/<int:flashcard_id>/delete/', views.delete_flashcard, name='delete_flashcard'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]

