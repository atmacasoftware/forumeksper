from django import forms
from server.models import RoomAnnouncement

class AnnouncementForm(forms.ModelForm):
	class Meta:
		model = RoomAnnouncement

		fields = [
			'title',
            'content',
		]

		labels = {
			'title': 'Duyuru Başlık',
			'content': 'Duyuru',
		}