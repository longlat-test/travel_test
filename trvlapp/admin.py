from django.contrib import admin

from .models import Profile, Folowers, Event, User, PasswordResetToken, Comments, Tags

class ProfileAdmin(admin.ModelAdmin):

      list_display = ('full_name', 'user', 'status', 'location', 'image', 'age' )
admin.site.register(Profile, ProfileAdmin )
admin.site.register(Folowers)
admin.site.register(Event)
admin.site.register(User)
admin.site.register(PasswordResetToken)
admin.site.register(Comments)
admin.site.register(Tags)



# Register your models here.
