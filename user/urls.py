from django.urls import path
from .views import RegisterView, login_view, logout_view, change_password

app_name = 'user'

urlpatterns = [
    #path('register/', register, name='register'),
     path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change_password/', change_password, name='change_password'),
]
