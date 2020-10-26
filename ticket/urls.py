from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_ticket, name="all_ticket"),
    path('login/', views.userLogin, name="login"),
    path('signup/', views.userSignup, name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path('create_ticket/', views.create_ticket, name="create_ticket"),
    path('single_ticket/<int:pk>', views.single_ticket, name="single_ticket"),
    path('update_ticket/<int:pk>/', views.update_ticket, name="update_ticket"),
]
