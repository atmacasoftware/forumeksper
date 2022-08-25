import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.paginator import Paginator
from django.db import transaction, IntegrityError
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
import threading

from django.template.loader import render_to_string

from notifications.models import Notification
from server.forms import AnnouncementForm
from server.models import Room, Message, MemberShip, RoomCategory, RoomAnnouncement, RoomManager, FavouriteMessage
from survey.forms import OptionsForm, SurveyForm
from survey.models import Options, Survey, Vote
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
    category = RoomCategory.objects.all()
    user_room = Room.objects.filter(user=request.user)
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
    return render(request, 'pages/chat/keşfet.html', {'rooms': rooms, 'messages': messages,'category':category,'user_room':user_room})

@login_required
def all_rooms(request):
    rooms = Room.objects.all()
    category = RoomCategory.objects.all()
    user_room = Room.objects.filter(user=request.user)
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
    return render(request,'pages/chat/discover_partials/all.html',{'rooms':rooms,'category':category,'user_room':user_room})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room).values('id', 'content', 'user__username',
                                                        'user__userprofile__profile_photo',
                                                        'date_added', 'file_type').order_by('-date_added')[:15]
    directs = Message.objects.filter(room=room).values('content', 'user__username', 'user__userprofile__profile_photo',
                                                       'date_added', 'file_type').order_by('-date_added')
    total_data = Message.objects.filter(room=room).count()
    room_participants = MemberShip.objects.filter(room=room)
    room_participants_count = MemberShip.objects.filter(room=room).count()
    room_manager = RoomManager.objects.filter(room=room)
    room_manager_count = RoomManager.objects.filter(room=room).count()
    participation_count = room_participants_count - room_manager_count
    all_profile = UserProfile.objects.all()
    participants = []
    managers = []
    managers_profile = []
    message_users = []
    profile = []
    owner_profile = []
    person_profile = None
    notification = None
    notification_count = None
    surveys = None
    options = None
    vote_option = None
    is_vote = False
    announcement = None
    favourite = None

    for a in all_profile:
        if room.user == a.user:
            owner_profile.append(a)

    for p in room_participants:
        participants.append(p.group_user)

    for rm in room_manager:
        managers.append(rm.user)

    for u in all_profile:
        for p in participants:
            if p.username == u.user.username:
                profile.append(u)
        for m in managers:
            if m.username == u.user.username:
                managers_profile.append(u)

    if request.user.is_authenticated:
        try:
            person_profile = UserProfile.objects.get(user=request.user)
            notification = Notification.objects.filter(recipient_user=request.user).order_by('-created_at')
            notification_count = Notification.objects.filter(recipient_user=request.user).count()
        except:
            return redirect('login')
    else:
        return redirect('login')

    OptionsFormset = modelformset_factory(Options, form=OptionsForm)
    form = SurveyForm(request.POST or None)
    formset = OptionsFormset(request.POST or None, queryset=Options.objects.none(), prefix='option')

    if "create_survey" in request.POST:
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    survey = form.save(commit=False)
                    survey.created_user = request.user
                    survey.room = room
                    survey.save()

                    for option in formset:
                        data = option.save(commit=False)
                        data.survey = survey
                        data.options_user = request.user
                        data.save()
            except IntegrityError:
                print("Error Encountered")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    try:
        surveys = Survey.objects.filter(room=room).order_by("-id")
        options = Options.objects.all()
    except:
        pass

    try:
        announcement = RoomAnnouncement.objects.filter(room=room).order_by('-id')
    except:
        announcement = "Duyuru bulunmamaktadır"

    announcement_forum = AnnouncementForm(request.POST or None)
    if "create_announcement" in request.POST:
        if form.is_valid():
            f_announcement = announcement_forum.save(commit=False)
            f_announcement.user = request.user
            f_announcement.room = room
            f_announcement.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        pass

    try:
        favourite = FavouriteMessage.objects.filter(room=room, user=request.user)
    except:
        pass

    return render(request, 'pages/chat/group_room.html',
                  {'room': room, 'directs': directs, 'messages': messages,
                   'room_participants_count': room_participants_count,
                   'room_participants': room_participants, 'all_profile': all_profile,
                   'participants': participants, 'profile': profile, 'owner_profile': owner_profile,
                   'person_profile': person_profile, 'notification': notification,
                   'notification_count': notification_count, 'form': form, 'formset': formset, 'surveys': surveys,
                   'options': options, 'vote_option': vote_option, 'announcement': announcement,
                   'announcement_forum': announcement_forum, 'managers_profile': managers_profile,
                   'room_manager_count': room_manager_count, 'participation_count': participation_count,
                   'favourite': favourite, 'total_data': total_data})


def json_room_message(request, slug):
    room = Room.objects.get(slug=slug)
    try:
        page_number_directs = request.POST.get('directspage')

        message = Message.objects.filter(room=room).order_by('-date_added').values(
            'id',
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


def json_survey(request, survey_id, option_id):
    try:
        survey = Survey.objects.get(id=survey_id)
        option = Options.objects.get(id=option_id)
        vote = Vote.objects.create(answered_user=request.user, survey=survey, options=option, is_answered=True)
        vote.save()

        vote_count = Vote.objects.filter(survey=survey).count()

        data = {
            'ok': 'ok',
        }

        if vote_count >= 1:
            data = {
                'ok': 'ok',
                'vote_count': vote_count
            }

        return JsonResponse({'data': data})
    except:
        pass


def json_survey_results(request, survey_id, option_id):
    res = None
    res_option = None
    survey = Survey.objects.filter(id=survey_id)
    options = Options.objects.filter(survey_id=survey_id)
    vote = Vote.objects.filter(survey_id=survey_id, options_id=option_id)
    vote_count = len(Vote.objects.filter(survey_id=survey_id))

    if len(survey) > 0 and len(options) > 0:
        data_survey = []
        data_option = []
        for s in survey:
            item = {
                'survey_id': s.id,
                'title': s.title,
                'countVote': s.countVote(),
            }
            data_survey.append(item)

        for o in options:
            option_item = {
                'option_id': o.id,
                'options': o.options,
                'countOptionVote': o.countOptionVote(),
                'rateVate': o.rateVate(),
                'countSurveyVote': o.countSurveyVote(),
            }
            data_option.append(option_item)

        res = data_survey
        res_option = data_option
    return JsonResponse({'data': res, 'data_option': res_option, 'vote_count': vote_count}, safe=False)


def json_option(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    options = list(
        Options.objects.filter(survey=survey).values('id', 'options', 'options_user_id', 'created_at', 'survey_id'))
    data = options
    return JsonResponse({'data': data}, safe=False)


def json_add_favourite_message(request, room_id, message_id):
    room = Room.objects.get(id=room_id)
    message = Message.objects.get(room_id=room_id, id=message_id)
    FavouriteMessage.objects.create(room=room, message=message, user=request.user)
    data = None
    try:
        get_message = list(
            FavouriteMessage.objects.filter(room=room, message=message).values('id', 'room', 'room_id', 'message',
                                                                               'message_id', 'message__user__username',
                                                                               'message__content'))
        if len(get_message) > 0:
            data = get_message
            return JsonResponse({'data': data}, safe=False)
    except:
        return HttpResponseRedirect(request.META['HTTP_REFERER'], {'data': data})


def load_more_msg(request, room_id):
    room = Room.objects.get(id=room_id)
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Message.objects.filter(room=room).values('id', 'content', 'user__username',
                                                        'user__userprofile__profile_photo',
                                                        'date_added', 'file_type').order_by('-date_added')[offset:offset + limit]
    t = render_to_string('pages/chat/ajax_message.html', {'data': data,'room':room})
    return JsonResponse({'data': t})
