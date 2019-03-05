from django.contrib import admin

from .models import Profile, Folowers

class ProfileAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'user', 'status', 'location', 'image', )
admin.site.register(Profile, ProfileAdmin )
admin.site.register(Folowers)



# Register your models here.
