from django.db import models
from birthday import BirthdayField, BirthdayManager

# Create your models here.
class Birthday(models.Model):
    name = models.CharField(default='', max_length=50)
    dob = BirthdayField()
    objects = BirthdayManager()

    def __str__(self):
        return f'{self.name} ({self.dob})'