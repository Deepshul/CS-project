from django.db import models

# Create your models here.

class Login(models.Model):
    sno=models.AutoField(primary_key=True)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)

'''class bookings(models.Model):
    sno=models.AutoField(primary_key=True)
    username=models.ForeignKey(login)
    show_code=models.CharField(max_length=50)'''

