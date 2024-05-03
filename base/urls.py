from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.login_, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),

   
    path('home/', views.home, name="home"),
    path("question/<str:pk>/", views.question, name="question"),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),


    path('update-question/<int:pk>', views.update_question, name='update-question'),

    path('delete-message/<int:pk>', views.delete_message, name='delete-message'),
    path('delete-question/<int:pk>', views.delete_question, name='delete-question'),
    path('delete-reply/<int:pk>', views.delete_reply, name='delete-reply'),


    path('update-user', views.update_user, name='update-user'),

    path('create-question/', views.create_question, name="create-question"),
]