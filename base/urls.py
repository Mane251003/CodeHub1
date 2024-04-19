from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
   
    path('home/', views.home, name="home"),
    path("question/<str:pk>/", views.question, name="question"),

    path('update-question/<int:pk>', views.update_question, name='update-question'),
    path('delete-question/<int:pk>', views.delete_question, name='delete-question'),
    path('create-question/', views.create_question, name="create-question"),

    
]