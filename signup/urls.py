from . import views
from django.urls import path,include

urlpatterns = [
    
    path('', views.home_view, name="home"),
    path('signup/', views.signup_view, name="signup"),
    path('login/',views.login_view,name="login"),
    path('login/<int:user_id>', views.user_view, name="profile"),
    path('edit/', views.profile_view, name="edit"),
    path('logout/',views.logout_view,name="logout"),
    #path('edit/<>', views.profile_view, name="profile"),
   
]