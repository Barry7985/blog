from django.urls import path

from .views import create_user, login_user, logout_view

app_name = 'accounts'

urlpatterns = [
    path('creation/', create_user, name='create'),
    path('login/', login_user, name='login'),
    path('logout/', logout_view, name='logout'),
]