from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from Utils.const import *
from Utils.functions import current_milli_time

#region User Account
def get_default_profile_image():
    return "profile_images/default/default_profile_image.png"

def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/profile_image.png'


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, user_type, password = None):
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse e-mail")
        if not username:
            username = first_name + '_' + str(current_milli_time())
        if not first_name:
            raise ValueError("L'utilisateur doit avoir un prenom")
        if not last_name:
            raise ValueError("L'utilisateur doit avoir un nom")
        if not user_type:
            raise ValueError("L'utilisateur doit avoir un user type")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name =  first_name.lower(),
            last_name = last_name.lower(),
            user_type = user_type,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, username, first_name, last_name, user_type, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name =  first_name.lower(),
            last_name = last_name.lower(),
            user_type = user_type,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
    

class UserAccount(AbstractBaseUser, PermissionsMixin):
    #required
    email = models.EmailField(verbose_name='email', max_length=EMAIL_LEN, unique = True)
    first_name = models.CharField(max_length=MAXCHAR)
    last_name = models.CharField(max_length=MAXCHAR)
    username = models.CharField(max_length=MAXCHAR, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    profile_image = models.ImageField(max_length=255, upload_to = get_profile_image_filepath, null = True, blank = True, default = get_default_profile_image)

    user_type = models.IntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_type', 'first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.last_name + ' ' + self.first_name
    
    def get_profile_image_filename(self): 
        index = str(self.profile_image).index(f'profile_images/{self.pk}/')
        return str(self.profile_image)[index:]

    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

#endregion

#region Members

class DoctorantModel(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    university = models.CharField(max_length=MAXCHAR)
    apogee = models.CharField(max_length=APOGEE_MAX)
    cin = models.CharField(max_length=CIN_MAX)

    def __str__(self):
        return self.user.email

class EncadrantModel(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    university = models.CharField(max_length=MAXCHAR)

    def __str__(self):
        return self.user.email

class MemberModel(models.Model):
    ENCADRANT = 0
    DOCTORANT = 1
    ADMIN = 2

    TYPES = (
        (ENCADRANT, 'ENCADRANT'),
        (DOCTORANT, 'DOCTORANT')
    )

    email = models.EmailField(unique=True)
    userType = models.IntegerField(choices= TYPES)
    date = models.DateTimeField(auto_now_add=True)
    signed = models.BooleanField(default= False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.email)

#endregion