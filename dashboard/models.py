from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    postal = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    postal = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    distance = models.FloatField(null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name