from django.urls import path
from .views import *

urlpatterns = [
    path('', forum_page, name="forum_page"),
    path('<slug:slug>', forum_details, name="forum_details"),
    path('json/yanıtla/<forum_id>/<comment_id>/', json_create_reply_comment, name="json_create_reply_comment"),
    path('json/begen/<forum_id>/', json_owner_like, name="json_owner_like"),
    path('json/forum/begenmeme/<forum_id>/', json_owner_dislike, name="json_owner_dislike"),
    path('json/yorum/begen/<comment_id>/', json_comment_like, name="json_comment_like"),
    path('json/yorum/begenmeme/<comment_id>/', json_comment_dislike, name="json_comment_dislike"),
]