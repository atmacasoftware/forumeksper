from django import forms

from forums.models import ForumComment


class ForumCommentForm(forms.ModelForm):
	class Meta:
		model = ForumComment

		fields = [
			'content',

		]
