from django.contrib import admin
from .models import appUser, Room, Room_request
# Register your models here.

@admin.register(appUser)
class appUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number','blocked_status')

@admin.register(Room)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('landlord', 'tenant', 'name')


@admin.register(Room_request)
class Paymentadmin(admin.ModelAdmin):
    list_display = ('from_user','status', 'room_id')