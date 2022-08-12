from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
import threading

from server.models import Room, Message, MemberShip, RoomCategory


@login_required
def rooms(request):
    rooms = Room.objects.filter(membership__group_user=request.user) or Room.objects.filter(user=request.user)
    category = RoomCategory.objects.all()
    if 'createChannels' in request.POST:
        try:
            postData = request.POST
            category = postData.get('category','')
            image = request.FILES.get("image")
            banner = request.FILES.get("banner")
            name = postData.get('name')
            private = postData.get('is_private','')

            get_cateogry = RoomCategory.objects.get(id=category)
            print(get_cateogry)

            if private == "1":
                private = False
            else:
                private = True
            data = Room.objects.create(name=name, user=request.user, category=get_cateogry, image=image, banner=banner, is_private=private)
            data.save()
            return redirect('room', data.slug)
        except:
            return render(request, 'pages/chat/rooms.html',{'rooms':rooms,'category':category})
    return render(request, 'pages/chat/rooms.html',{'rooms':rooms,'category':category})


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
