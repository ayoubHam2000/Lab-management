from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

from Utils.const import *
from Utils.functions import current_milli_time, getFileName, getUserTypeName, getUserTypeNameFromGroup
from django.contrib.auth.models import Group

from PIL import Image
import os

# from django import template
# register = template.Library()

#region User Account
def get_default_profile_image():
    return "default/default_profile_image.png"

def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/profile_image.png'


class MyUserManager(BaseUserManager):
    def create_user(self, email, group, first_name='', last_name='', password = None):
        if email == None:
            raise ValueError("L'utilisateur doit avoir une adresse e-mail")
        
        username = 'user_' + str(current_milli_time())
        group = Group.objects.get(name = group)
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using = self._db)
        user.groups.add(group)
        return user
    
    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            group='superadmin',
            first_name = first_name,
            last_name = last_name
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_signed = True

        encadrant = EncadrantModel(user = user)
        encadrant.save()

        user.save(using = self._db)
        return user

# keep one image in the server
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
    first_name = models.CharField(max_length=MAXCHAR, blank=True)
    last_name = models.CharField(max_length=MAXCHAR, blank=True)
    username = models.CharField(max_length=MAXCHAR, unique=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_signed = models.BooleanField(default=False)
    profile_image = models.ImageField(
        max_length=255, 
        storage=OverwriteStorage(), 
        upload_to = get_profile_image_filepath, 
        null = True, 
        blank = True, 
        default = get_default_profile_image
        )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.getFullName()
    
    def get_profile_image_filename(self): 
        index = str(self.profile_image).index(f'profile_images/{self.pk}/')
        return str(self.profile_image)[index:]

    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    # Me ===============================================
    # Me ===============================================

    def getImage(self):
        return f'/media/{self.profile_image}'

    def isAdmin(self):
        return self.groups.filter(name__in = [ADMIN, SUPERADMIN]).exists()

    def isSuperAdmin(self):
        return self.groups.filter(name=SUPERADMIN).exists()
    
    def isEncadrant(self):
        return self.groups.filter(name__in = [ENCADRANT, ADMIN, SUPERADMIN]).exists()
    
    def isEncadrantPure(self):
        return self.groups.filter(name__in = [ENCADRANT]).exists()

    def isDoctorant(self):
        return self.groups.filter(name = DOCTORANT).exists()

    def getFullName(self):
        return f'{self.first_name} {self.last_name}'

    def getUserTypeName(self):
        return getUserTypeNameFromGroup(self)

    def userSwitchAdmin(self):
        # activate or deativate admin
        groupAdmin = Group.objects.get(name = 'admin')
        groupEncadrant = Group.objects.get(name = 'encadrant')
        if self.groups.filter(name=ENCADRANT).exists():
            self.groups.clear()
            self.groups.add(groupAdmin)
        elif self.groups.filter(name=ADMIN).exists():
            self.groups.clear()
            self.groups.add(groupEncadrant)
        
    def hasAccount(self):
        if self.isEncadrant():
            hasAccount = EncadrantModel.objects.filter(user = self)
            return hasAccount.exists()
        elif self.isDoctorant():
            hasAccount = DoctorantModel.objects.filter(user = self)
            return hasAccount.exists()
        return False

    def allowSwitchAdmin(self, requestUser):
        assert isinstance(requestUser, UserAccount)
        if requestUser.email != self.email and requestUser.isSuperAdmin():
            if self.isEncadrant():
                return True
        return False


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
    university = models.IntegerField(choices=UNIVERSITIES, default=0)
    apogee = models.CharField(max_length=APOGEE_MAX)
    cin = models.CharField(max_length=CIN_MAX)
    these = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.email

class EncadrantModel(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    university = models.IntegerField(choices=UNIVERSITIES, default=0)

    def __str__(self):
        return self.user.email

 
class RelationModel(models.Model):
    TYPES = (
        (0, 'ENCADRANT'),
        (1, 'CO.ENCADRANT')
    )
    user1 = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserAccount, null=False, related_name='doctorant_encadrant', on_delete=models.CASCADE) 
    relationType = models.IntegerField(choices=TYPES, default = 0)

    def __str__(self):
        return f'{self.user1.email}->{self.user2.email}'
    
    def _relationType(self):
        return self.getRelationName()

    def getRelationName(self):
        return self.TYPES[self.relationType][1]

    def getEncadrant(user):
        assert isinstance(user, UserAccount)
        if user.isDoctorant():
            r = RelationModel.objects.filter(user1=user, relationType = 0)
            if r.exists():
                return r[0].user2
        return None

    def isValide(self):
        user1 = self.user1
        user2 = self.user2
        relationType = self.relationType

        if user1.email == user2.email:
            return False, 'même email'
        if user1.isEncadrant() and user2.isEncadrant():
            return False, 'impossible d\'associer encadrant à encadrant'
        if user1.isDoctorant() and user2.isDoctorant():
            return False, 'impossible d\'associer doctorant à doctorant'
 
        relation_exist = RelationModel.objects.filter(user1 = user1, user2 = user2)
        if relation_exist.exists():
            return False, 'La relation existe déjà'

        if relationType == 0:
            hasEncadrant = None
            if user1.isDoctorant():
                hasEncadrant = RelationModel.objects.filter(user1=user1, relationType=0)
            if user2.isDoctorant():
                hasEncadrant = RelationModel.objects.filter(user1=user2, relationType=0)
            if hasEncadrant.exists():
                return False, 'A déjà un encadrant'
        
        return True,''
        


#endregion