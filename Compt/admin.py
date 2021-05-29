from django.contrib import admin

from .models import PostModel, PostCommentModel

admin.site.register(PostModel)
admin.site.register(PostCommentModel)

