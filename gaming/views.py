from django.shortcuts import render

# Create your views here.

def game_mainpage(request):
    return render(request,'pages/game/mainpage.html')
