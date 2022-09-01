from django.db import models

# Create your models here.

class users(models.Model):
    username=models.CharField(max_length=64)
    password=models.CharField(max_length=64)
    email=models.CharField(max_length=64)


    def __str__(self):
        return f"user_id : {self.id} ,  username :  {self.username} ,    E-mail  :  {self.email}"

class staff(models.Model):
    username=models.CharField(max_length=64)
    password=models.CharField(max_length=64)
    email=models.CharField(max_length=64)
    role=models.CharField(max_length=64)
    def __str__(self):
        return f"{self.id} : {self.username} and {self.password} and {self.email} and {self.role}"

    
class mega(models.Model):
    username=models.CharField(max_length=64)
    password=models.CharField(max_length=64)
    def __str__(self):
        return f"{self.id} is {self.username}"
class sports(models.Model):
    sport=models.CharField(max_length=64)
    def __str__(self):
        return f"{self.id} : {self.sport}"

class arena(models.Model):
    arena=models.CharField(max_length=64)
    def __str__(self):
        return f"{self.id} : {self.arena}"

class slots(models.Model):
    start_time=models.TimeField()
    end_time=models.TimeField()

    def __str__(self):
        return f"{self.id} : from {self.start_time} to {self.end_time}"

class data(models.Model):
    user_id=models.IntegerField()
    sport_id=models.IntegerField()
    arena_id=models.IntegerField()
    slot_id=models.IntegerField()
    def __str__(self):
        return f"{self.id} : user with id={self.user_id} is registered for sport with id={self.sport_id} on arena with id={self.arena_id} in a slot of id={self.slot_id}"

class ava_data(models.Model):
    sport_id=models.IntegerField()
    arena_id=models.IntegerField()
    slot_id=models.IntegerField()
    def __str__(self):
        return f"{self.id} : sport with id={self.sport_id} and arena_id={self.arena_id} and slot_id={self.slot_id} is available."