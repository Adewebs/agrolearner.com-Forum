from django.urls import path
from . import views

urlpatterns= [
    path('', views.home, name='homepage'),
    path('room/<int:pk>/', views.room, name='room'),
    path('create-room/' , views.create_room, name='create-room'),
    path('editroom/<int:pk>', views.updateroom, name='editroom'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('register/', views.registerpage, name='register'),
    path('converdelete/<int:pk>', views.conversationdelete, name='converdelete'),
    path('profile/<int:pk>', views.userprofile, name='profile'),
    path('edituser/', views.edituser, name='edituser'),
path('topics/', views.topicspage, name='topics'),
path('mactivity/', views.mobileactivity, name='mactivity'),
]