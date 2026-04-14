from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('profile/', views.profile, name='Profile'),
    path('login/', views.login, name='Login'),
    path('logout/', views.logout_view, name='Logout'),
    path('register/', views.register, name='Register'),
    path('forgot-password/', views.forgot_pass, name='ForgotPassword'),

    path('blog/', views.blog , name='Blog'),
    path('blog/<int:id>/', views.blogdetails, name='BlogDetails'),
]

