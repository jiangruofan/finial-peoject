from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateUserSerializer, GetAllUserInfoSerializer, GetUserInfoSerializer, ChangePasswordSerializer, StudyPlanSerializer, AddPointsSerializer, AddTimeSerializer
from .serializers import CreateRoomSerializer, GetRoomInfoSerializer, GetAllCategorySerializer
from .models import User, ClassRoom, StudyCategory
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
        password = request.GET.get("password")
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

            data = GetUserInfoSerializer(user).data
            data["classRoom"] = user.classRoom.name if user.classRoom else None

            return Response(data, status=status.HTTP_200_OK)

        return Response({'Bad Request': 'email or password not found in request'}, status=status.HTTP_400_BAD_REQUEST)


class GetUserInfo(APIView):
    
    def get(self, request):
        email = request.GET.get('email')

        if not email:
            return Response({'Bad Request': 'email not found in request'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email)
        if not user:
            return Response({'User Not Found in Database': 'Invalid ID.'}, status=status.HTTP_404_NOT_FOUND)
        user = user[0]

        data = GetUserInfoSerializer(user).data
        data["classRoom"] = user.classRoom.name if user.classRoom else None

        return Response(data, status=status.HTTP_200_OK)



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

    def put(self, request):
        serialize = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            user = User.objects.filter(email=email)
            if not user:
                return Response({'msg': 'User does not exists.'}, status=status.HTTP_403_FORBIDDEN)
            user = user[0]
            user.weeklyPoints += serializer.data.get('weeklyPoints')
            user.totalPoints += serializer.data.get('totalPoints')
            user.save()
            return Response(AddPointsSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class AddTime(APIView):
    serializer_class = AddTimeSerializer

    def put(self, request):
        serialize = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            user = User.objects.filter(email=email)
            if not user:
                return Response({'msg': 'User does not exists.'}, status=status.HTTP_403_FORBIDDEN)
            user = user[0]
            user.completedToday += serializer.data.get('completedToday')
            user.completedWeek += serializer.data.get('completedWeek')
            user.save()
            return Response(AddTimeSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class CreateRoom(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            user = User.objects.filter(email=email)
            if not user:
                return Response({'msg': 'User does not exists.'}, status=status.HTTP_403_FORBIDDEN)
            user = user[0]

            name = serializer.data.get('name')
            if ClassRoom.objects.filter(name=name):
                return Response({'msg': 'Classroom already exists.'}, status=status.HTTP_403_FORBIDDEN)

            description = serializer.data.get('description')
            maxPeople = max(serializer.data.get('maxPeople') or 1, 1)
            passWord = serializer.data.get('passWord')

            studyCategory = StudyCategory.objects.filter(name=serializer.data.get("studyCategory"))
            if not studyCategory:
                studyCategory = StudyCategory(name=serializer.data.get("studyCategory"))
                studyCategory.save()
            else:
                studyCategory = studyCategory[0]
            
            classRoom = ClassRoom(name=name, description=description, maxPeople=maxPeople, passWord=passWord, studyCategory=studyCategory)
            classRoom.save()

            user.classRoom = classRoom
            user.save()

            return Response({'Message': 'Success'}, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):

    def put(self, request):
        email = request.GET.get('email')
        roomName = request.GET.get('roomName')
        if email and roomName:
            user = User.objects.filter(email=email)
            if not user:
                return Response({'msg': 'User does not exists.'}, status=status.HTTP_403_FORBIDDEN)
            user = user[0]

            classRoom = ClassRoom.objects.filter(name=roomName)
            if not classRoom:
                return Response({'msg': 'ClassRoom does not exists.'}, status=status.HTTP_403_FORBIDDEN)
            classRoom = classRoom[0]

            if classRoom.curPeople == classRoom.maxPeople:
                return Response({'msg': 'ClassRoom is already full.'}, status=status.HTTP_403_FORBIDDEN)

            classRoom.curPeople += 1
            classRoom.save()
            user.classRoom = classRoom
            user.save()

            return Response({'Message': 'Success'}, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class LeaveRoom(APIView):

    def put(self, request):
        email = request.GET.get('email')
        if email:
            user = User.objects.filter(email=email)
            if not user:
                return Response({'msg': 'User does not exists.'}, status=status.HTTP_403_FORBIDDEN)
            user = user[0]

            if user.classRoom and user.classRoom.curPeople == 1:
                user.classRoom.delete()
            user.classRoom = None
            return Response({'Message': 'Success'}, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class GetRoomInfo(APIView):

    def get(self, request):
        name = request.GET.get('name')
        if name:
            room = ClassRoom.objects.filter(name=name)
            if not room:
                return Response({'msg': 'Room does not exists.'}, status=status.HTTP_403_FORBIDDEN)
            room = room[0]
            data = GetRoomInfoSerializer(room).data
            data["studyCategory"] = room.studyCategory.name
            data["users"] = []
            for user in room.user_set.all():
                data["users"].append(user.email)

            return Response(data, status=status.HTTP_200_OK)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class GetRoomByStudyCategory(APIView):

    def get(self, request):
        studyCategory = request.GET.get("studyCategory")
        if studyCategory:
            studyCategory = StudyCategory.objects.filter(name=studyCategory)
            if not studyCategory:
                return Response({'msg': 'StudyCategory does not exists.'}, status=status.HTTP_403_FORBIDDEN)
            studyCategory = studyCategory[0]
            for room in studyCategory.classroom_set.all():
                data = GetRoomInfoSerializer(room).data
                data["studyCategory"] = room.studyCategory.name
                data["users"] = []
                for user in room.user_set.all():
                    data["users"].append(user.email)
            return Response(data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class GetAllUsers(APIView):

    def get(self, request):
        users = User.objects.all()
        data = []
        for user in users:
            data1 = GetAllUserInfoSerializer(user).data
            data1["classRoom"] = user.classRoom.name if user.classRoom else None
            data.append(data1)
        return Response(data, status=status.HTTP_200_OK)


class GetAllCategory(APIView):

    def get(self, request):
        categories = StudyCategory.objects.all()
        data = []
        for category in categories:
            data.append(GetAllCategorySerializer(category).data)
        return Response(data, status=status.HTTP_200_OK)
        
        


















            






