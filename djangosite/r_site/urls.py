from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('profile/', views.profile, name='Profile'),
    path('profile/avatar/', views.update_avatar, name='UpdateAvatar'),
    path('login/', views.login, name='Login'),
    path('logout/', views.logout_view, name='Logout'),
    path('register/', views.register, name='Register'),
    path('forgot-password/', views.forgot_pass, name='ForgotPassword'),

    path('post/create/', views.create_post, name='CreatePost'),
    path('post/<int:post_id>/like/', views.like_post, name='LikePost'),
    path('post/<int:post_id>/comment/', views.add_comment, name='AddComment'),
    path('post/<int:post_id>/delete/', views.delete_post, name='DeletePost'),

    path('blog/', views.blog, name='Blog'),
    path('blog/<int:id>/', views.blogdetails, name='BlogDetails'),
]
