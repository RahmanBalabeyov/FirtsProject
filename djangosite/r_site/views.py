from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.core.exceptions import ValidationError


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


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
