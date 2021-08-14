from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from states.register_state import RegisterUser
from .models import User, Car, Province, Region, Ads

admin.site.register(Car)
admin.site.register(Province)


@admin.register(Ads)
class FilteredAds(admin.ModelAdmin):
    list_display = ['Driver', 'From', 'To', 'scheduled_date']
    list_filter = ['Driver', 'status']


@admin.register(User)
class FilteredUser(admin.ModelAdmin):
    list_display = ['Name', 'Phone_number', 'Car', 'Joined_date']
    list_filter = ['Is_registered', 'Is_Driver']


@admin.register(Region)
class FilteredProvince(admin.ModelAdmin):
    list_filter = ['Province']
