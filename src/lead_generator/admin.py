from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'url', 'created_at')
    list_filter = ('created_at',)
