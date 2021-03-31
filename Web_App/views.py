from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
from Web_App.SetupGame import StartSetup
from Web_App.StartGame import Start
from Web_App.models import BoundingBoxes
from Web_App.Direct_Keys import *


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


def start_setup_car(request):
    cam = StartSetup()
    Result_Setup_car = cam.get_frame()
    res = BoundingBoxes()
    res.Game_Name = GameName
    res.Face = list_to_string(Result_Setup_car[0])
    res.Switches = listoflists_to_string(Result_Setup_car[1])
    res.save()
    # request.session['id'] = res.id
    return render(request, 'game_car.html')


def start_game_car(request):
    temp = Start(request)
    return render(request, 'game_car.html')


def start_setup_mortal(request):
    cam = StartSetup()
    Result_Setup_mortal = cam.get_frame()
    res = BoundingBoxes()
    res.Game_Name = GameName
    res.Face = list_to_string(Result_Setup_mortal[0])
    res.Switches = listoflists_to_string(Result_Setup_mortal[1])
    res.save()
    # request.session['id'] = res.id
    return render(request, 'game_mortal.html')


def start_game_mortal(request):
    temp = Start(request)
    return render(request, 'game_mortal.html')
