from django.urls import path
from .views import CreateUser, Login, GetUserInfo, ChangePassword, CreateStudyPlan, AddPoints, AddTime, CreateRoom, JoinRoom
from .views import LeaveRoom, GetRoomInfo, GetRoomByStudyCategory, GetAllUsers, GetAllCategory

urlpatterns = [
    path('createUser', CreateUser.as_view()),
    path("login", Login.as_view()),
    path("getUserInfo", GetUserInfo.as_view()),
    path("changePassword", ChangePassword.as_view()),
    path("createStudyPlan", CreateStudyPlan.as_view()),
    path("addPoints", AddPoints.as_view()),
    path("addTime", AddTime.as_view()),
    path("createRoom", CreateRoom.as_view()),
    path("joinRoom", JoinRoom.as_view()),
    path("leaveRoom", LeaveRoom.as_view()),
    path("getRoomInfo", GetRoomInfo.as_view()),
    path("getRoomByStudyCategory", GetRoomByStudyCategory.as_view()),
    path("getAllUsers", GetAllUsers.as_view()),
    path("getAllCategory", GetAllCategory.as_view()),

]