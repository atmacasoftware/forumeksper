from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
import threading

from server.models import Room, Message, MemberShip

@login_required
def rooms(request):
    rooms = Room.objects.filter(membership__group_user=request.user) or Room.objects.filter(user=request.user)
    return render(request, 'pages/chat/rooms.html',{'rooms':rooms})


@login_required
def room_find(request):
    rooms = Room.objects.all()
    if 'is_join' in request.POST:
        try:
            postData = request.POST
            room_slug = postData.get('room_slug')
            get_user = postData.get('request_user')
            room = Room.objects.get(slug=room_slug)
            user = User.objects.get(username=get_user)
            MemberShip.objects.create(group_user=user, room=room)
            return redirect('rooms')
        except:
            pass
    return render(request, 'pages/chat/keşfet.html',{'rooms':rooms,'messages':messages})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]
    return render(request, 'pages/chat/room.html',{'room':room,'messages':messages})
