from django.db import models

from Account.models import UserAccount
from Utils.const import *
from Utils.functions import current_milli_time

from Utils.functions import getTimeFormat

def images_path(instance, name):
    return f'post_files/{instance.user.pk}/{name}'

class PostModel(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    post = models.TextField()
    date = models.DateTimeField(verbose_name='date', auto_now_add=True)
    imge = models.ImageField(max_length=255, upload_to = images_path, null = True, blank = True)

    def __str__(self):
        return self.post
    
    def getImage(self):
        if self.imge:
            return '/media/' + self.imge.name
        return '' 
    
    def getDate(self):
        return getTimeFormat(self.date)

class PostCommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.EmailField(max_length=EMAIL_LEN)
    text = models.TextField()
    date = models.DateTimeField(verbose_name='date', auto_now_add=True)

    def __str__(self):
        return self.text
    
    def getUser(self):
        user = UserAccount.objects.get(email = self.user)
        return user
    
    def getDate(self):
        return getTimeFormat(self.date)

