from django.urls import path

#from django.contrib.auth.views import LoginView


from .views import (
    LoginView,
    MemberManagement,
    LogoutView,
    HomeView,
    CheckEmailView,
    MemberRegister,
    AccountUpdate,
)

app_name = 'Account'

urlpatterns = [
    path('', HomeView.as_view()),
    path('login/', LoginView.as_view(), name = 'login'),
    path('members/', MemberManagement.as_view(), name = 'addMember'),
    path('members/<theType>/', MemberManagement.as_view(), name = 'memberInfo'),
    path('members/<str:userType>/<int:accountId>/', AccountUpdate.as_view(), name = 'updateAccount'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('home/', HomeView.as_view(), name = 'home'),
    path('checkEmail/', CheckEmailView.as_view(), name = 'checkEmail'),
    path('MemberRegister/<uidb64>/<token>/', MemberRegister.as_view(), name = 'memberRegister'),
]