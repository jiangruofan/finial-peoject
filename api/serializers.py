from rest_framework import serializers
from .models import User, ClassRoom, StudyCategory

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'passWord', 'studyCategory')

class GetAllUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class GetUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', "email", "studyCategory", "classRoom", 'weeklyPoints',
         'totalPoints', 'completedToday', "completedWeek", "goalToday", "goalWeek",
         "plan_Monday", "plan_Tuesday", "plan_Wednesday", "plan_Thursday", "plan_Friday", "plan_Saturday", "plan_Sunday")

class ChangePasswordSerializer(serializers.ModelSerializer):
    newPassWord = serializers.CharField(max_length=32)
    class Meta:
        model = User
        fields = ('email', 'passWord', "newPassWord")

class StudyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "plan_Monday", "plan_Tuesday", "plan_Wednesday", "plan_Thursday", "plan_Friday", "plan_Saturday", "plan_Sunday")

class AddPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", 'weeklyPoints', 'totalPoints')


class AddTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", 'completedToday', "completedWeek")

class CreateRoomSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    studyCategory = serializers.CharField(max_length=32)
    class Meta:
        model = ClassRoom
        fields = ("name", "description", "maxPeople", "passWord", "email", "studyCategory")
        
class GetRoomInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = "__all__"

class GetAllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyCategory
        fields = "__all__"
