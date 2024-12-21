from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('createpost', createpost, name='createpost'),
    path('viewpost/<int:post_id>', viewpost, name='viewpost'),
    path('login', LoginUser.as_view(), name='login'),
    path('register', RegisterUser.as_view(), name='register'),
    path('logout', LogoutUser, name='logout'),
    path('postlist', post_list, name='postlist'),
    path('deletepost/<int:post_id>', delete_post, name='deletepost'),
    path('changepost/<int:post_id>', changepost, name='changepost'),
    path('checkpassword', checkpassword, name='checkpassword'),
]
