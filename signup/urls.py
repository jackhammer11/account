from . import views
from django.urls import path,include

urlpatterns = [
    
    path('', views.home_view, name="home"),
    path('signup/', views.signup_view, name="signup"),
   
]