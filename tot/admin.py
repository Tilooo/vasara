#tot/admin.py

from django.contrib import admin
from .models import Language, Set, Box, Flashcard

admin.site.register(Language)
admin.site.register(Set)
admin.site.register(Box)
admin.site.register(Flashcard)

