from django.urls import path
from base import views


urlpatterns = [
    path('', views.home, name="homePage"),
    path('test/', views.test, name="testPage"),
]
