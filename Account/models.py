from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from Utils.const import *
from Utils.functions import current_milli_time, getFileName
from PIL import Image
import os
from django.core.files.storage import FileSystemStorage


#region User Account
def get_default_profile_image():
    return "default/default_profile_image.png"

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

# keep one image in the saerver
class OverwriteStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name, *args, **kwargs):
        return name

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
    profile_image = models.ImageField(
        max_length=255, 
        storage=OverwriteStorage(), 
        upload_to = get_profile_image_filepath, 
        null = True, 
        blank = True, 
        default = get_default_profile_image
        )

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
    
    def getImage(self):
        return f'/media/{self.profile_image}'

    def isAdmin(self):
        return self.groups.filter(name='admin').exists()
    
    def isEncadrant(self):
        return self.groups.filter(name='encadrant').exists() or self.isAdmin()
    
    def getFullName(self):
        return f'{self.first_name} {self.last_name}'

    def getUserType(self):
        if self.user_type == 0 or self.user_type == 2:
            return 'encadrant'
        elif self.user_type == 1:
            return 'doctorant'
        return ''

    def save(self, *args, **kwargs):
        newWidth = 400
        # reduce quality image
        super(UserAccount, self).save(*args, **kwargs)
        if(os.path.isfile(self.profile_image.path)):
            image = Image.open(self.profile_image.path)
            width = image.width
            height = image.height
            ratio = width / height
            output_size = (width, newWidth / ratio)
            # resize and save
            image.thumbnail(output_size)
            image.save(self.profile_image.path)

    

#endregion

#region Members

class DoctorantModel(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    university = models.CharField(max_length=MAXCHAR)
    apogee = models.CharField(max_length=APOGEE_MAX)
    cin = models.CharField(max_length=CIN_MAX)
    these = models.TextField(blank=True)

    def __str__(self):
        return self.user.email

class EncadrantModel(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    university = models.CharField(max_length=MAXCHAR)

    def __str__(self):
        return self.user.email

from django import template
register = template.Library()

class MemberModel(models.Model):
    ENCADRANT = 0
    DOCTORANT = 1
    ADMIN = 2

    TYPES = (
        (ENCADRANT, 'ENCADRANT'),
        (DOCTORANT, 'DOCTORANT')
    )

    email = models.EmailField(unique=True)
    userType = models.IntegerField(choices= TYPES, default = 1)
    date = models.DateTimeField(auto_now_add=True)
    signed = models.BooleanField(default= False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.email)
    
    def getImage(self):
        user = UserAccount.objects.filter(email = self.email)
        if user.exists():
            return '/media/' + user[0].profile_image.name
        return '/media/' + get_default_profile_image()

    def getStatus(self):
        if not self.signed:
            return 2
        else:
            if self.active:
                return 1
            else:
                return 0
    
    def getUserType(self):
        return MemberModel.TYPES[self.userType][1]
    


class DoctorantRelation(models.Model):
    ENCADRANT = 0
    CO_ENCADRANT = 1

    TYPES = (
        (ENCADRANT, 'ENCADRANT'),
        (CO_ENCADRANT, 'CO.ENCADRANT')
    )
    doctorant = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    encadrant = models.EmailField()
    userType = models.IntegerField(choices= TYPES, default = 0)

    def __str__(self):
        return self.doctorant.email
    
    def getEncadrant(self):
        return UserAccount.objects.get(email = self.encadrant)

    def isValide(doctorant, encadrant, relationType):
        if encadrant.user_type == MemberModel.DOCTORANT:
            return False, 'impossible d\'ajouter doctorant comme Co.encadrant'
        encadrant = encadrant.email
        
        sameRelation = DoctorantRelation.objects.filter(doctorant = doctorant, encadrant = encadrant)
        if sameRelation.exists():
            return False, 'La relation existe déjà'
        
        hasEncadrant = DoctorantRelation.objects.filter(doctorant = doctorant, userType = 0)
        if hasEncadrant.exists() and relationType == 0:
            return False, 'A déjà un encadrant'
        
        return True,''
        
    


#endregion