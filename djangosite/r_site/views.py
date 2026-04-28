from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Like, Comment, Profile


@login_required
def index(request):
    posts = Post.objects.select_related('author', 'author__profile').prefetch_related('likes', 'comments__user', 'comments__user__profile').all()
    liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
    return render(request, 'index.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
    })


@login_required
@require_POST
def create_post(request):
    caption = request.POST.get('caption', '').strip()
    image = request.FILES.get('image')
    if not caption and not image:
        messages.error(request, 'Paylaşım üçün şəkil və ya yazı əlavə edin.')
        return redirect('Home')
    Post.objects.create(author=request.user, caption=caption, image=image)
    messages.success(request, 'Paylaşım uğurla əlavə olundu.')
    return redirect('Home')


@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': post.like_count})


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = request.POST.get('text', '').strip()
    if not text:
        return JsonResponse({'ok': False, 'error': 'Şərh boş ola bilməz.'}, status=400)
    comment = Comment.objects.create(user=request.user, post=post, text=text)
    profile = comment.user.profile
    return JsonResponse({
        'ok': True,
        'comment': {
            'id': comment.id,
            'text': comment.text,
            'username': comment.user.username,
            'avatar_url': profile.avatar_url,
            'initials': profile.initials,
        },
        'count': post.comment_count,
    })


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Paylaşım silindi.')
    return redirect('Profile')


@login_required
def profile(request):
    user = request.user
    user_posts = Post.objects.filter(author=user).prefetch_related('likes', 'comments')
    liked_posts = Post.objects.filter(likes__user=user).select_related('author', 'author__profile').distinct()
    user_comments = Comment.objects.filter(user=user).select_related('post', 'post__author').order_by('-created_at')
    return render(request, 'profile.html', {
        'profile_user': user,
        'user_posts': user_posts,
        'liked_posts': liked_posts,
        'user_comments': user_comments,
    })


@login_required
@require_POST
def update_avatar(request):
    avatar = request.FILES.get('avatar')
    if not avatar:
        messages.error(request, 'Şəkil seçin.')
        return redirect('Profile')
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    profile_obj.avatar = avatar
    profile_obj.save()
    messages.success(request, 'Profil şəkli yeniləndi.')
    return redirect('Profile')


def login(request):
    if request.user.is_authenticated:
        return redirect('Home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, 'Uğurla daxil oldunuz.')
            return redirect('Home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('Home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Qeydiyyat uğurla tamamlandı.')
            return redirect('Home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('Login')


def forgot_pass(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not password1 or not password2:
            messages.error(request, 'Bütün xanaları doldurun.')
        elif password1 != password2:
            messages.error(request, 'Şifrələr uyğun gəlmir.')
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'Belə bir istifadəçi tapılmadı.')
            else:
                try:
                    validate_password(password1, user)
                except ValidationError as e:
                    for err in e.messages:
                        messages.error(request, err)
                else:
                    user.set_password(password1)
                    user.save()
                    messages.success(request, 'Şifrə uğurla yeniləndi. İndi daxil ola bilərsiniz.')
                    return redirect('Login')
    return render(request, 'forgot-password.html')


@login_required
def blog(request):
    return render(request, 'blog.html')


@login_required
def blogdetails(request, id):
    return render(request, 'blog-details.html', {'blog_id': id})
