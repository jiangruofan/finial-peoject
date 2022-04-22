import email
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from yaml import serialize
from .serializers import CreateUserSerializer, CreateUserSerializer_full, GetUserInfoSerializer, ChangePasswordSerializer, StudyPlanSerializer, AddPointsSerializer, AddTimeSerializer
from .models import User
from datetime import date


# Create your views here.
class CreateUser(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            queryset = User.objects.filter(email=email)
            if queryset.exists():
                return Response({'msg': 'User already exists.'}, status=status.HTTP_403_FORBIDDEN)
            name = serializer.data.get('name')
            passWord = serializer.data.get('passWord')
            studyCategory = serializer.data.get("studyCategory")
            user = User(name=name, email=email, passWord=passWord, studyCategory=studyCategory, loginTime=date.today())
            user.save()
            return Response(GetUserInfoSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    def get(self, request):
        email = request.GET.get('email')
        password = request.GET["password"]
        if email and password:
            user = User.objects.filter(email=email)
            if not user:
                return Response({'User Not Found in Database': 'Invalid ID.'}, status=status.HTTP_404_NOT_FOUND)
            user = user[0]
            if user.passWord != password:
                return Response({'msg': 'password is not correct'}, status=status.HTTP_403_FORBIDDEN)
            
            judge = False
            time1 = user.loginTime
            if time1.year != date.today().year or time1.month != date.today().month or time1.day != date.today().day:
                judge = True
                user.completedToday = 0
                user.weeklyPoints += 30
                user.totalPoints += 30
                user.loginTime = date.today()
            
            diff = date.today() - time1
            if time1.isoweekday() + diff.days > 7:
                judge = True
                user.weeklyPoints = 0
                user.completedWeek = 0

            if judge:
                user.save()

            return Response(GetUserInfoSerializer(user).data, status=status.HTTP_200_OK)
        else:
            Response({'Bad Request': 'email or password not found in request'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            queryset = User.objects.filter(email=email)
            if not queryset:
                return Response({'Email Not Found in Database': 'Invalid Email.'}, status=status.HTTP_404_NOT_FOUND)
            oldpassword = serializer.data.get("passWord")
            if oldpassword != queryset[0].passWord:
                return Response({'msg': 'password is not correct'}, status=status.HTTP_403_FORBIDDEN)
            queryset[0].passWord = serializer.data.get("newPassWord")
            queryset[0].save()
            return Response({'Message': 'Success'}, status=status.HTTP_200_OK)
        else:
            Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class CreateStudyPlan(APIView):
    serializer_class = StudyPlanSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            user = User.objects.filter(email=email)

            if not user:
                return Response({'msg': 'User does not exists.'}, status=status.HTTP_403_FORBIDDEN)

            user = user[0]

            user.plan_Monday = serializer.data.get('plan_Monday')
            user.plan_Tuesday = serializer.data.get('plan_Tuesday')
            user.plan_Wednesday = serializer.data.get('plan_Wednesday')
            user.plan_Thursday = serializer.data.get('plan_Thursday')
            user.plan_Friday = serializer.data.get('plan_Friday')
            user.plan_Saturday = serializer.data.get('plan_Saturday')
            user.plan_Sunday = serializer.data.get('plan_Sunday')
            user.save()
            return Response(StudyPlanSerializer(user).data, status=status.HTTP_200_OK)

        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class AddPoints(APIView):
    serializer_class = AddPointsSerializer

    def post(self, request):
        serialize = self.serializer_class(data=request.data)
        
        













            






