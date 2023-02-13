from django.db import models
from django.contrib.auth.models import User
from birthday import BirthdayField, BirthdayManager
# Create your models here.

class IdentityCard(models.Model):
    picture = models.ImageField(default="/profile_pic/default.webp/", blank=True, upload_to='identity_card_pics/')
    name = models.CharField(default="", max_length=60)
    standard = models.CharField(default="", max_length=10)
    division = models.CharField(default="", max_length=10)
    gr_no = models.IntegerField(default="")
    gender = models.CharField(default="", max_length=10)
    dob = BirthdayField()
    contact = models.IntegerField(default="")
    address = models.CharField(default="", max_length=200)
    aadhaar = models.IntegerField(default="")
    objects = BirthdayManager()
    
    def __str__(self):
        namestr = f"{self.name.title()} - {self.standard.upper()}-{self.division} ({self.gr_no})"
        return namestr


class PasswordCollector(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    password = models.CharField(default='', max_length=50)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}\'s password has been collected!'


class Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    class_teacher = models.CharField(default="v", max_length=5)
    division = models.CharField(default="a", max_length=2)
    gender = models.CharField(default="xx", max_length=3)
    profile_picture = models.ImageField(upload_to='profile_pic/', default='')
    
    def __str__(self):
        return f'{self.user.username} ({self.user.first_name + " " + self.user.last_name})'


class Contact(models.Model):
    name = models.CharField(default='', max_length=50)
    date = models.DateTimeField(auto_now=True, blank=True)
    email = models.EmailField(default='')
    message = models.TextField()
    def __str__(self):
        return f"{self.name}'s contact on {self.date}"



class Attendance(models.Model):
    duration = models.DateTimeField(auto_now=True, blank=True)
    date = models.CharField(default='', max_length=100)
    student = models.ForeignKey(IdentityCard, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        student = self.student
        return f'{str(student)} ------- {self.date}'
