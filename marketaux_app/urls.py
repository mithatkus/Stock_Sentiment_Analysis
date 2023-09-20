from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sentiment/', views.sentiment_route, name='sentiment_route'),
]
