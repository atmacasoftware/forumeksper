from django import forms
from .models import Survey, Options

class SurveyForm(forms.ModelForm):
	class Meta:
		model = Survey

		fields = [
			'title',
		]

		labels = {
			'title': 'Anket Sorusu',
		}


class OptionsForm(forms.ModelForm):
	class Meta:
		model = Options

		fields = [
			'options',
		]

		labels = {
			'options': 'Seçenekler',
		}

		widgets = {
			'options': forms.TextInput(attrs={'class': 'formset-field','required':'required'})
		}