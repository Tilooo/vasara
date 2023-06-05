#tot/models.py

from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Set(models.Model):
    name = models.CharField(max_length=100)
    languages = models.ManyToManyField(Language)

    def __str__(self):
        return self.name


class Box(models.Model):
    name = models.CharField(max_length=100)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    box = models.ForeignKey(Box, on_delete=models.CASCADE)

    def __str__(self):
        return self.question
