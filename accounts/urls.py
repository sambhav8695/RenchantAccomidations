from django.urls import path
from .views import *


urlpatterns = [
    path('signup', signup, name='signup'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
]
