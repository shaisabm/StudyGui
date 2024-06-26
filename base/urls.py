from django.urls import path
from . import views


urlpatterns = [
    path('', views.home,name="home"),
    path('room/<int:pk>/', views.room,name="room"),
    path('create-room/', views.createRoom,name="create-room"),
    path('update-room/<int:pk>', views.updateRoom,name="update-room"),
    path('delete-room/<int:pk>', views.deleteRoom,name="delete-room"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('delete-message/<int:pk>/', views.deleteMessage, name="delete-message"),
    path('profile/<str:pk>/', views.userProfile, name="profile"),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('delete-user/',views.delete_user,name = 'delete-user'),

]
