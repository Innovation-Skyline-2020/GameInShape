from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def games(request):
    return render(request, 'games.html')

def about_us(request):
    return render(request, 'about_us.html')