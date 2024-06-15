from django.contrib import admin
from .models import Stock
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Stock)
class StockAdmin(ImportExportModelAdmin):
    list_display = ("symbol", "date", "price")