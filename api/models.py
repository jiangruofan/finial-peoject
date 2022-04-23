from django.db import models

# Create your models here.
class StudyCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    maxPeople = models.IntegerField(default=1)
    curPeople = models.IntegerField(default=1)
    passWord = models.CharField(max_length=15, null=True, blank=True)
    studyCategory = models.ForeignKey(StudyCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    passWord = models.CharField(max_length=15)
    studyCategory = models.CharField(max_length=20)
    loginTime = models.DateField()
    weeklyPoints = models.IntegerField(default=30)
    totalPoints = models.IntegerField(default=30)
    completedToday = models.IntegerField(default=0)
    completedWeek = models.IntegerField(default=0)
    goalToday = models.IntegerField(default=0)
    goalWeek = models.IntegerField(default=0)
    plan_Monday = models.IntegerField(default=0)
    plan_Tuesday = models.IntegerField(default=0)
    plan_Wednesday = models.IntegerField(default=0)
    plan_Thursday = models.IntegerField(default=0)
    plan_Friday = models.IntegerField(default=0)
    plan_Saturday = models.IntegerField(default=0)
    plan_Sunday = models.IntegerField(default=0)
    classRoom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True,  blank=True)
    





