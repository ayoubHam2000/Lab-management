from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.files.storage import FileSystemStorage

from Utils.const import *
from Utils.functions import current_milli_time, getFileName, getUserTypeName, getUserTypeFromGroup

from PIL import Image
import os


#region User Account
def get_default_profile_image():
    return "default/default_profile_image.png"

def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/profile_image.png'


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password = None):
        if email == None:
            raise ValueError("L'utilisateur doit avoir une adresse e-mail")
        if username == None:
            username = first_name + '_' + str(current_milli_time())
        if first_name == None:
            raise ValueError("L'utilisateur doit avoir un prenom")
        if last_name == None:
            raise ValueError("L'utilisateur doit avoir un nom")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name =  first_name.lower(),
            last_name = last_name.lower()
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name =  first_name.lower(),
            last_name = last_name.lower(),
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
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


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

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
    
    # Me ===============================================
    # Me ===============================================

    def getImage(self):
        return f'/media/{self.profile_image}'

    def isAdmin(self):
        return self.groups.filter(name__in = ['admin', 'superadmin']).exists()

    def isSuperAdmin(self):
        return self.groups.filter(name='superadmin').exists()
    
    def isEncadrant(self):
        return self.groups.filter(name__in = ['encadrant', 'admin', 'superadmin']).exists()
    
    def isDoctorant(self):
        return self.groups.filter(name = 'doctorant').exists()

    def getFullName(self):
        return f'{self.first_name} {self.last_name}'

    def getUserType(self):
        return getUserTypeFromGroup(self)


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

class MemberModel(models.Model):
    TYPES = (
        (ENCADRANT, 'ENCADRANT'),
        (DOCTORANT, 'DOCTORANT'),
        (ADMIN, 'ADMIN'),
    )

    email = models.EmailField(unique=True)
    userType = models.IntegerField(choices= TYPES, default = 1)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user = models.OneToOneField(UserAccount, null=True, related_name='user_member', on_delete=models.SET_NULL) 
    signed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.email)
    
    def hasAccount(self):
        return self.user != None
  
    def isEncadrant(self):
        return self.userType in [ADMIN, ENCADRANT, SUPERADMIN]
    
    def isDoctorant(self):
        return self.userType == DOCTORANT

    def isAdmin(self):
        return self.userType == ADMIN

    def getUserType(self):
        return getUserTypeName(self.userType)
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)
     
class DoctorantRelation(models.Model):
    TYPES = (
        (ENCADRANT, 'ENCADRANT'),
        (CO_ENCADRANT, 'CO.ENCADRANT')
    )
    doctorant = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    encadrant = models.ForeignKey(UserAccount, null=False, related_name='doctorant_encadrant', on_delete=models.CASCADE) 
    relationType = models.IntegerField(choices= TYPES, default = 0)

    def __str__(self):
        return self.doctorant.email
    
    def getRelationName(self):
        return self.TYPES[self.relationType][1]

    def isValide(self):
        doctorant = self.doctorant
        encadrant = self.encadrant
        relationType = self.relationType

        if doctorant.email == encadrant.email:
            return False, 'même email'
        if not doctorant.isDoctorant():
            return False, 'impossible d\'associer encadrant à encadrant'
        if not encadrant.isEncadrant():
            return False, 'impossible d\'associer doctorant à doctorant'

        sameRelation = DoctorantRelation.objects.filter(doctorant = doctorant, encadrant = encadrant)
        if sameRelation.exists():
            return False, 'La relation existe déjà'

        if relationType == 0:
            hasEncadrant = DoctorantRelation.objects.filter(doctorant = doctorant, relationType = 0)
            if hasEncadrant.exists():
                return False, 'A déjà un encadrant'
        
        return True,''
        


#endregion