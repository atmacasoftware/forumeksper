from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
import threading

from server.models import Room, Message, MemberShip, RoomCategory
from user_account.models import UserProfile


@login_required
def rooms(request):
    rooms = Room.objects.filter(membership__group_user=request.user)
    owner_rooms = Room.objects.filter(user=request.user)
    category = RoomCategory.objects.all()
    if 'createChannels' in request.POST:
        try:
            postData = request.POST
            category = postData.get('category', '')
            image = request.FILES.get("image")
            banner = request.FILES.get("banner")
            name = postData.get('name')
            private = postData.get('is_private', '')

            get_cateogry = RoomCategory.objects.get(id=category)

            if private == "1":
                private = False
            else:
                private = True
            data = Room.objects.create(name=name, user=request.user, category=get_cateogry, image=image, banner=banner,
                                       is_private=private)
            data.save()
            return redirect('room', data.slug)
        except:
            messages.info(request,
                          'Kategori seçimi, kanal kapak resmi, kanal banner resmi, kanal adı ve kanal gizlilik durumunu seçmeniz gerekmektedir.')
            return render(request, 'pages/chat/rooms.html',
                          {'rooms': rooms, 'category': category, 'messages': messages, 'owner_rooms': owner_rooms})
    return render(request, 'pages/chat/rooms.html', {'rooms': rooms, 'category': category, 'owner_rooms': owner_rooms})


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
    return render(request, 'pages/chat/keşfet.html', {'rooms': rooms, 'messages': messages})


@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room).values('content', 'user__username', 'user__userprofile__profile_photo',
                                                        'date_added', 'file_type').order_by('-date_added')
    directs = Message.objects.filter(room=room).values('content', 'user__username', 'user__userprofile__profile_photo',
                                                       'date_added', 'file_type').order_by('-date_added')
    room_participants = MemberShip.objects.filter(room=room)
    room_participants_count = MemberShip.objects.filter(room=room).count()
    participants = []
    message_users = []
    profile = []

    paginator_directs = Paginator(directs, 15)
    page_number_directs = request.GET.get('directspage')
    directs_data = paginator_directs.get_page(page_number_directs)

    paginator_messages = Paginator(messages, 15)
    page_number_messages = request.GET.get('messagespage')
    messages_data = paginator_messages.get_page(page_number_messages)

    for p in room_participants:
        participants.append(p.group_user)

    return render(request, 'pages/chat/single_room.html',
                  {'room': room, 'directs': directs_data, 'messages': messages_data,
                   'room_participants_count': room_participants_count,
                   'room_participants': room_participants})


def json_room_message(request, slug):
    room = Room.objects.get(slug=slug)
    try:
        page_number_directs = request.POST.get('directspage')

        message = Message.objects.filter(room=room).order_by('-date_added').values(
            'content',
            'user__username',
            'date_added',
            'file_type',
            'user__userprofile__profile_photo',
        )

        all_message_count = message.count()

        # Pagination for directs
        paginator_directs = Paginator(message, 15)

        if paginator_directs.num_pages >= int(page_number_directs):
            directs_data = paginator_directs.get_page(page_number_directs)

            # Creating the list of data
            directs_list = list(directs_data)

            return JsonResponse(directs_list, safe=False)
        else:
            return JsonResponse({'empty': True}, safe=False)
    except:
        return JsonResponse({'empty': True}, safe=False)
