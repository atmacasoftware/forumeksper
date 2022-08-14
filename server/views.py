from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
import threading

from server.models import Room, Message, MemberShip, RoomCategory
from user_account.models import UserProfile


@login_required
def rooms(request):
    rooms = Room.objects.filter(membership__group_user=request.user)
    print(rooms)
    owner_rooms = Room.objects.filter(user=request.user)
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

            if private == "1":
                private = False
            else:
                private = True
            data = Room.objects.create(name=name, user=request.user, category=get_cateogry, image=image, banner=banner, is_private=private)
            data.save()
            return redirect('room', data.slug)
        except:
            messages.info(request,
                          'Kategori seçimi, kanal kapak resmi, kanal banner resmi, kanal adı ve kanal gizlilik durumunu seçmeniz gerekmektedir.')
            return render(request, 'pages/chat/rooms.html',{'rooms':rooms,'category':category,'messages':messages,'owner_rooms':owner_rooms})
    return render(request, 'pages/chat/rooms.html',{'rooms':rooms,'category':category,'owner_rooms':owner_rooms})


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
    messages = Message.objects.filter(room=room)
    room_participants = MemberShip.objects.filter(room=room)
    room_participants_count = MemberShip.objects.filter(room=room).count()
    participants = []
    message_users = []
    profile = []
    message_users_profile = []

    for p in room_participants:
        participants.append(p.group_user)

    for pu in participants:
        profile.append(UserProfile.objects.filter(user=pu))

    for m in messages:
        message_users.append(m.user)

    for mu in message_users:
        message_users_profile.append(UserProfile.objects.filter(user=mu))

    return render(request, 'pages/chat/single_room.html',{'room':room,'messages':messages,'room_participants_count':room_participants_count,'room_participants':room_participants,'profile':profile})
