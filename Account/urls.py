from django.urls import path

#from django.contrib.auth.views import LoginView


from .views import (
    LoginView,
    LogoutView,
    HomeView,
    UsersManagement,
    CheckEmailView,
    UserRegister,
    AccountUpdate,
    ChangePassword,
)

app_name = 'Account'

urlpatterns = [
    path('', HomeView.as_view()),
    path('login/', LoginView.as_view(), name = 'login'),
    path('usersManagement/', UsersManagement.as_view(), name = 'usersManagement'),
    path('usersManagement/<theType>/', UsersManagement.as_view(), name = 'usersManagement_type'),
    path('changePassword/<int:userId>/', ChangePassword.as_view(), name = 'changePassword'),
    path('user/update/<int:accountId>/', AccountUpdate.as_view(), name = 'updateAccount'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('home/', HomeView.as_view(), name = 'home'),
    path('checkEmail/', CheckEmailView.as_view(), name = 'checkEmail'),
    path('userRegister/<uidb64>/<token>/', UserRegister.as_view(), name = 'userRegister'),
]