from django.urls import path

from .views import (
    PostsView,
    CommentView
)

app_name = 'Compt'

urlpatterns = [
    path('posts/', PostsView.as_view(), name = 'posts'),
    path('posts/<str:theType>/', PostsView.as_view(), name = 'postsType'),
    path('comment/<int:id>/', CommentView.as_view(), name = 'comment'),
]