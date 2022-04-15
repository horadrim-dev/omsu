from tkinter import CASCADE
from django.db import models

# Create your models here.
class Menu(models.Model):
    title = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    parent = models.ForeignKey('Menu', on_delete=models.CASCADE,blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title
    