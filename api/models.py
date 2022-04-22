from django.db import models

# Create your models here.
class StudyCategory(models.Model):
    name = models.CharField(max_length=20, null=False)


class ClassRoom(models.Model):
    name = models.CharField(max_length=20, null=False)
    description = models.CharField(max_length=100, default="")
    studyCategory = models.ForeignKey(StudyCategory, on_delete=models.CASCADE)


class User(models.Model):
    name = models.CharField(max_length=20, null=False)
    email = models.EmailField(null=False)
    passWord = models.CharField(max_length=15, null=False)
    studyCategory = models.CharField(max_length=20, null=False)
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
    





