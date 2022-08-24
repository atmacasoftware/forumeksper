from import_export import resources
from .models import Citys


class CityResource(resources.ModelResource):
    class Meta:
        model = Citys
        fields = (
            'id',
            'name',
        )
