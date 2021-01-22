from django.shortcuts import render

def home(request):
    return render(request, 'front_web_1.html')

def game_page(request):
    return render(request, 'game_page.html')

def game_car(request):
    return render(request, 'game_car.html')

def game_mortal(request):
    return render(request, 'game_mortal.html')

def about_us(request):
    return render(request, 'about_us.html')