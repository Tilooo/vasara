#tot/forms.py

from django import forms
from .models import Set, Box, Flashcard


class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['name', 'boxs']


class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['name']


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['question', 'answer']
