from import_export import resources
from .models import Citys,Weather


class CityResource(resources.ModelResource):
    class Meta:
        model = Citys
        fields = (
            'id',
            'name',
        )

class WeatherResource(resources.ModelResource):
    class Meta:
        model = Weather
        fields = (
            'id',
            'user',
            'city',
            'ip',
        )