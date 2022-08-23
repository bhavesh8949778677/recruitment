from django.db import models

# Create your models here.

class users(models.Model):
    username=models.CharField(max_length=64)
    password=models.CharField(max_length=64)
    email=models.CharField(max_length=64)


    # def __str__(self):
    #     return f"user_id : {self.id} ,  username :  {self.username} ,    E-mail  :  {self.email}"

class staff(models.Model):
    username=models.CharField(max_length=64)
    password=models.CharField(max_length=64)
    email=models.CharField(max_length=64)
    role=models.CharField(max_length=64)

    
class mega(models.Model):
    username=models.CharField(max_length=64)
    password=models.CharField(max_length=64)
    # def __str__(self):
    #     return f"Username is {self.username}"
class sports(models.Model):
    sport=models.CharField(max_length=64)

class slots(models.Model):
    days=models.CharField(max_length=64)
    start_time=models.TimeField()
    end_time=models.TimeField()

