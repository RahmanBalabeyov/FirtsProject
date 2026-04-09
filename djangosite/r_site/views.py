from django.shortcuts import render

def index(request):
    # 'index.html' faylını göstər
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'login.html')

def register(request):  
    return render(request, 'register.html')

def forgot_pass(request):   
    return render(request, 'forgot-password.html')

def blog(request):
    return render(request, 'blog.html')

def blogdetails(request, id):
    # 'id' dəyişənini HTML-ə göndəririk
    return render(request, 'blog-details.html', {'blog_id': id})