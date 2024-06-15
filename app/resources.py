from django.http import HttpResponse
from import_export import resources
from .models import Stock

class StockResources(resources.ModelResource):
    class Meta:
        model = Stock