from django.urls import path

#from django.contrib.auth.views import LoginView


from .views import (
    TestView,
    LoginView,
    AddMember,
    LogoutView,
    HomeView,
    CheckEmailView,
    MemberRegister,
)

app_name = 'Account'

urlpatterns = [
    path('', TestView.as_view(), name = 'test'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('members/', AddMember.as_view(), name = 'addMember'),
    path('members/<theType>/', AddMember.as_view(), name = 'memberInfo'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('home/', HomeView.as_view(), name = 'home'),
    path('checkEmail/', CheckEmailView.as_view(), name = 'checkEmail'),
    path('MemberRegister/<uidb64>/<token>/', MemberRegister.as_view(), name = 'memberRegister'),
]