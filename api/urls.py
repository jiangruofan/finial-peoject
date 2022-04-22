from django.urls import path
from .views import CreateUser, Login, ChangePassword, CreateStudyPlan

urlpatterns = [
    path('createUser', CreateUser.as_view()),
    path("login", Login.as_view()),
    path("changePassword", ChangePassword.as_view()),
    path("CreateStudyPlan", CreateStudyPlan.as_view()),

]