#tot/views.py

from django.shortcuts import render, get_object_or_404
from .models import Set, Box, Flashcard


def set_list(request):
    sets = Set.objects.all()
    return render(request, 'tot/set_list.html', {'sets': sets})


def box_detail(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    return render(request, 'tot/box_detail.html', {'box': box})


def flashcard_detail(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
    return render(request, 'tot/flashcard_detail.html', {'flashcard': flashcard})

