from django.contrib import admin
from users.models import Location, User

admin.site.register(Location)
admin.site.register(User)

# class LocationAdmin(admin.ModelAdmin):
#     pass
#
#
# class UserAdmin(admin.ModelAdmin):
#     pass
#