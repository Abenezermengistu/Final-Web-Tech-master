from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user_history/', views.user_history, name='user_history')
]
