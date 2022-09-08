from django import forms
from mainpage.models import Weather


class WeatherForm(forms.ModelForm):
    class Meta:
        model = Weather
        fields = ['city']
