from django.urls import path
from . import views


urlpatterns = [
    path('',views.gerRoutes),
    path('rooms/',views.getRooms),
    path('rooms/<int:pk>',views.getRoom)

]