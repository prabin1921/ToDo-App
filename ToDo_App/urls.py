from django.urls import path
from . import views
from .views import*

from django.contrib.auth.views import LogoutView
 
urlpatterns = [
    path('login/', LogIn.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(next_page='/login'), name = 'logout'),
    path('register/', RegisterPage.as_view(), name = 'register'),
    
    path('', TaskView.as_view(), name ='tasks'),
    path('task/<int:pk>/', taskDetail.as_view(), name ='task'),
    path('create/', createTask.as_view(), name = 'create'),
    path('update/<int:pk>/', UpdateTask.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteTask.as_view(), name='delete'),

]
