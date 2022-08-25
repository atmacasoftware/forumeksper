from django.urls import path
from server.views import *

urlpatterns = [
    path('', rooms, name="rooms"),
    path('<slug:slug>/', room, name='room'),
    path('json/<slug:slug>/', json_room_message, name='json_room_message'),
    path('json/message/<room_id>/', load_more_msg, name='load_more_msg'),
    path('kesfet/hepsi/', all_rooms, name='all_rooms'),
    path('anket-cevabi/<survey_id>/<option_id>/', json_survey, name='json_survey'),
    path('anket-secenekleri/<survey_id>/', json_option, name='json_option'),
    path('anket-cevabi/anket-sonuclari/<survey_id>/<option_id>/', json_survey_results, name='json_survey_results'),
    path('favorilere-ekle/<room_id>/<message_id>/', json_add_favourite_message, name='json_add_favourite_message'),
]
