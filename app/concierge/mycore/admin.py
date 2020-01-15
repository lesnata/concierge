# Register your models here.
from django.conf import settings
from django.contrib import admin

from .models import Tenant, Room, Journal


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'phone')
    search_fields = ('first_name', 'last_name', 'phone', 'date_of_birth')
    list_filter = ('date_of_birth', 'last_name')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'max_guests', 'owner', 'status')
    search_fields = ('number', 'max_guests', 'owner', 'status')
    list_filter = ('owner', 'number')


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'tenant_id', 'guests', 'notes', 'key_out_date', 'key_in_date', 'is_kept')
    search_fields = ('room_number', 'tenant_id', 'guests', 'notes', 'key_out_date', 'key_in_date', 'is_kept')
    list_filter = ('room_number', 'is_kept')
