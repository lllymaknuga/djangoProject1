from django.urls import path

from .views import CustomUserCreateView, PhonNumberOtpCodeGenerate, CustomUserViewList, PhonNumberOtpCodeValidate, UpdateUsername, DeleteUser

urlpatterns = [
    path('create/', CustomUserCreateView.as_view()),
    path('generate/', PhonNumberOtpCodeGenerate.as_view()),
    path('validate/', PhonNumberOtpCodeValidate.as_view()),
    path('list/', CustomUserViewList.as_view()),
    path('update_username/', UpdateUsername.as_view()),
    path('delete/', DeleteUser.as_view())
]