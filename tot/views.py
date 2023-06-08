from django.shortcuts import render, get_object_or_404, redirect
from .models import Set, Box, Flashcard
from .forms import SetForm, BoxForm, FlashcardForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def set_list(request):
    sets = Set.objects.all()
    return render(request, 'tot/set_list.html', {'sets': sets})

def set_detail(request, set_id):
    set_obj = get_object_or_404(Set, pk=set_id)
    return render(request, 'tot/set_detail.html', {'set': set_obj})


def box_detail(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    return render(request, 'tot/box_detail.html', {'box': box})


def flashcard_detail(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
    return render(request, 'tot/flashcard_detail.html', {'flashcard': flashcard})


def create_set(request):
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tot:set_list')
    else:
        form = SetForm()
    return render(request, 'tot/create_set.html', {'form': form})


@login_required
def create_box(request, set_id):
    set_obj = get_object_or_404(Set, pk=set_id)
    boxes = set_obj.boxes.all()  # Retrieve boxes associated with the set
    if request.method == 'POST':
        form = BoxForm(request.POST)
        if form.is_valid():
            box = form.save(commit=False)
            box.set = set_obj
            box.save()
            return redirect('tot:box_detail', box_id=box.id)
    else:
        form = BoxForm()
    return render(request, 'tot/create_box.html', {'form': form, 'set': set_obj})


def create_flashcard(request, box_id):
    box_obj = get_object_or_404(Box, pk=box_id)
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.box = box_obj
            flashcard.save()
            return redirect('tot:box_detail', box_id=box_id)
    else:
        form = FlashcardForm()
    return render(request, 'tot/create_flashcard.html', {'form': form, 'box': box_obj})


def edit_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
    box_obj = flashcard.box
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect('tot:box_detail', box_id=box_obj.id)
    else:
        form = FlashcardForm(instance=flashcard)
    return render(request, 'tot/edit_flashcard.html', {'form': form, 'box': box_obj})


def delete_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
    box_obj = flashcard.box
    if request.method == 'POST':
        flashcard.delete()
        return redirect('tot:box_detail', box_id=box_obj.id)
    return render(request, 'tot/delete_flashcard.html', {'flashcard': flashcard})


def flashcard_detail(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
    return render(request, 'tot/flashcard_detail.html', {'flashcard': flashcard})


@login_required
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tot:set_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def home(request):
    return render(request, 'tot/home.html')
