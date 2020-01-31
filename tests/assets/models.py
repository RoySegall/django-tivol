from django.db import models
from django.db.models import CharField, IntegerField, DateTimeField


class Animal(models.Model):
    animal_name = CharField(max_length=25)
    sound = CharField(max_length=25)
    number_of_legs = IntegerField()

    def __str__(self):
        return self.animal_name
