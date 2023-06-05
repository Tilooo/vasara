#tot/urls.py

from django.urls import path
from . import views

app_name = 'tot'

urlpatterns = [
    path('', views.set_list, name='set_list'),
    path('box/<int:box_id>/', views.box_detail, name='box_detail'),
    path('flashcard/<int:flashcard_id>/', views.flashcard_detail, name='flashcard_detail'),
]



