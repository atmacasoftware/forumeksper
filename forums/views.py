from django.db.models import Count, Max, Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from forums.models import ForumCategory, Forum, ForumView, ForumComment, ReplyComment, LikeForum, DisLikeForum, \
    LikeComment, DisLikeComment, EditorSelectForum, UserForumPoint
from user_account.models import UserProfile


# Create your views here.

def forum_page(request):
    categoris = ForumCategory.objects.all()
    forum = None
    all_forums = None
    editor_select = None

    try:
        all_forums = Forum.objects.all().annotate(popular_forum=Count('forum_views')).distinct().order_by(
            '-popular_forum')[:10]
    except:
        all_forums = Forum.objects.all().annotate(popular_forum=Count('forum_views')).distinct().order_by(
            '-popular_forum')
    try:
        forum = Forum.objects.all()[:7]
    except:
        forum = Forum.objects.all()
    try:
        editor_select = EditorSelectForum.objects.all().order_by('-created_at')[:10]
    except:
        editor_select = EditorSelectForum.objects.all().order_by('-created_at')

    if 'crete_subject' in request.POST:
        postData = request.POST
        category_id = postData.get('category_id')
        category = get_object_or_404(ForumCategory, id=category_id)
        title = postData.get('title')
        content = postData.get('content')

        data = Forum.objects.create(user=request.user, category=category, title=title, content=content, status=True)
        data.save()
        point = UserForumPoint.objects.filter(user=request.user).exists()
        if point == True:
            user = UserForumPoint.objects.get(user=request.user)
            update_user = UserForumPoint.objects.filter(user=request.user).update(point=int(user.point) + 100)
            update_user.save()
        else:
            user = UserForumPoint.objects.create(user=request.user, point=100)
            user.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    context = {
        'categoris': categoris,
        'forum': forum,
        'all_forums': all_forums,
        'editor_select': editor_select,
    }

    return render(request, 'pages/forum/forums.html', context)


def forum_details(request, slug):
    forum = get_object_or_404(Forum, slug=slug)
    ip = request.META['REMOTE_ADDR']
    all_profile = UserProfile.objects.all()
    owner_profile = UserProfile.objects.get(user__username=forum.user.username)
    comment = ForumComment.objects.filter(forum=forum)
    reply_comment = ReplyComment.objects.filter(forums=forum)
    all_forums = None
    editor_select = None
    comment_data = []

    try:
        editor_select = EditorSelectForum.objects.all().order_by('-created_at')[:10]
    except:
        editor_select = EditorSelectForum.objects.all().order_by('-created_at')

    try:
        all_forums = Forum.objects.all().annotate(popular_forum=Count('forum_views')).distinct().order_by(
            '-popular_forum')[:10]
    except:
        all_forums = Forum.objects.all().annotate(popular_forum=Count('forum_views')).distinct().order_by(
            '-popular_forum')

    for cd in comment:
        item = {
            'user': cd.user,
            'id': cd.id,
            'content': cd.content,
            'created_at': cd.created_at,
            'isLiked': cd.isLikedComment(request),
            'isLikedCountComment': cd.isLikedCountComment(),
            'isDisliked': cd.dislikedComment(request),
            'dislikedCountComment': cd.dislikedCountComment(),
            'ReplyCommentCount': cd.ReplyCommentCount(),
            'editor_select': editor_select,
        }

        comment_data.append(item)

    if not ForumView.objects.filter(forum=forum, session=request.session.session_key):
        view = ForumView(forum=forum, ip_address=ip, session=request.session.session_key)
        view.save()
    forum_views = ForumView.objects.filter(forum=forum).count()

    if 'create_comment' in request.POST:
        postData = request.POST
        comment = postData.get('comment')
        ip = request.META.get('REMOTE_ADDR')
        data = ForumComment.objects.create(user=request.user, forum=forum, content=comment, ip=ip)
        data.save()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    if 'reply_create_comment' in request.POST:
        postData = request.POST
        comment_id = postData.get('comment_id')
        related_comment = get_object_or_404(ForumComment, id=comment_id)
        content = postData.get('reply_comment')
        ip = request.META.get('REMOTE_ADDR')
        data = ReplyComment.objects.create(user=request.user, forums=forum, comment=related_comment, content=content,
                                           ip=ip)
        data.save()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    context = {
        'forum': forum,
        'forum_views': forum_views,
        'owner_profile': owner_profile,
        'comment': comment,
        'all_profile': all_profile,
        'reply_comment': reply_comment,
        'comment_data': comment_data,
        'all_forums': all_forums,
    }

    return render(request, 'pages/forum/forum_details.html', context)


def json_create_reply_comment(request, forum_id, comment_id):
    pass


def json_owner_like(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    ip = request.META.get('REMOTE_ADDR')
    like = LikeForum.objects.filter(forum=forum, user=request.user).exists()
    data = None

    if like == False:
        dislike = DisLikeForum.objects.filter(forum=forum, user=request.user).exists()

        if dislike == False:
            like = LikeForum.objects.create(forum=forum, user=request.user, ip=ip, is_liked=True)
            like.save()
            data = 'liked'

        elif dislike == True:
            dislike = DisLikeForum.objects.filter(forum=forum, user=request.user)
            dislike.delete()
            like = LikeForum.objects.create(forum=forum, user=request.user, ip=ip, is_liked=True)
            like.save()
            data = 'deleted_dislike_create_liked'

    elif like == True:
        like = LikeForum.objects.filter(forum=forum, user=request.user, ip=ip)
        like.delete()
        data = 'deleted'
    return JsonResponse({'data': data})


def json_owner_dislike(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    ip = request.META.get('REMOTE_ADDR')
    dislike = DisLikeForum.objects.filter(forum=forum, user=request.user).exists()
    data = None

    if dislike == False:
        like = LikeForum.objects.filter(forum=forum, user=request.user).exists()
        if like == False:
            dislike = DisLikeForum.objects.create(forum=forum, user=request.user, ip=ip, is_liked=True)
            dislike.save()
            data = 'disliked'
        elif like == True:
            like = LikeForum.objects.filter(forum=forum, user=request.user)
            like.delete()
            dislike = DisLikeForum.objects.create(forum=forum, user=request.user, ip=ip, is_liked=True)
            dislike.save()
            data = 'deleted_liked_create_dislike'
    elif dislike == True:
        dislike = DisLikeForum.objects.filter(forum=forum, user=request.user, ip=ip)
        dislike.delete()
        data = 'deleted'

    return JsonResponse({'data': data})


def json_comment_like(request, comment_id):
    comment = get_object_or_404(ForumComment, id=comment_id)
    ip = request.META.get('REMOTE_ADDR')
    like = LikeComment.objects.filter(comment=comment, user=request.user).exists()
    data = None

    if like == False:
        dislike = DisLikeComment.objects.filter(comment=comment, user=request.user).exists()

        if dislike == False:
            like = LikeComment.objects.create(comment=comment, user=request.user, ip=ip, is_liked=True)
            like.save()
            data = 'liked'

        elif dislike == True:
            dislike = DisLikeComment.objects.filter(comment=comment, user=request.user)
            dislike.delete()
            like = LikeComment.objects.create(comment=comment, user=request.user, ip=ip, is_liked=True)
            like.save()
            data = 'deleted_dislike_create_liked'

    elif like == True:
        like = LikeComment.objects.filter(comment=comment, user=request.user, ip=ip)
        like.delete()
        data = 'deleted'
    return JsonResponse({'data': data})


def json_comment_dislike(request, comment_id):
    comment = get_object_or_404(ForumComment, id=comment_id)
    ip = request.META.get('REMOTE_ADDR')
    dislike = DisLikeComment.objects.filter(comment=comment, user=request.user).exists()
    data = None

    if dislike == False:
        like = LikeComment.objects.filter(comment=comment, user=request.user).exists()
        if like == False:
            dislike = DisLikeComment.objects.create(comment=comment, user=request.user, ip=ip, is_liked=True)
            dislike.save()
            data = 'disliked'
        elif like == True:
            like = LikeComment.objects.filter(comment=comment, user=request.user)
            like.delete()
            dislike = DisLikeComment.objects.create(comment=comment, user=request.user, ip=ip, is_liked=True)
            dislike.save()
            data = 'deleted_liked_create_dislike'
    elif dislike == True:
        dislike = DisLikeComment.objects.filter(comment=comment, user=request.user, ip=ip)
        dislike.delete()
        data = 'deleted'

    return JsonResponse({'data': data})


def popular(request):
    all_forums = None
    try:
        all_forums = Forum.objects.all().annotate(popular_forum=Count('forum_views')).distinct().order_by(
            '-popular_forum')[:10]
    except:
        all_forums = Forum.objects.all().annotate(popular_forum=Count('forum_views')).distinct().order_by(
            '-popular_forum')

    context = {
        'all_forums': all_forums,
    }

    return render(request, 'pages/forum/popular.html', context)


def editor_select(request):
    editor_select = None
    try:
        editor_select = EditorSelectForum.objects.all().order_by('-created_at')[:10]
    except:
        editor_select = EditorSelectForum.objects.all().order_by('-created_at')

    context = {
        'editor_select': editor_select,
    }

    return render(request, 'pages/forum/editor_select.html', context)
