from django.contrib import admin

from .models import Profile, Folowers, Event, User

class ProfileAdmin(admin.ModelAdmin):

      list_display = ('full_name', 'user', 'status', 'location', 'image' )
admin.site.register(Profile, ProfileAdmin )
admin.site.register(Folowers)
admin.site.register(Event)
admin.site.register(User)



# Register your models here.
