from django import forms
from .models import Stock

class StockData(forms.Form):
	class meta:
		model = Stock
		fields = '__all__'