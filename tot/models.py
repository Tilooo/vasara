from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Set(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, unique=True, default='default_identifier')  # Add default value
    languages = models.ManyToManyField(Language)
    boxes = models.ManyToManyField('Box', related_name='sets')

    def __str__(self):
        return self.name


class Box(models.Model):
    name = models.CharField(max_length=100)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.set.name})"


class Flashcard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    image = models.ImageField(upload_to='flashcard_images/', blank=True, null=True)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)

    def __str__(self):
        return self.question
