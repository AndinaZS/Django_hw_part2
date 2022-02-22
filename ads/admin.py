from django.contrib import admin
from ads.models import Location, User, Advert, Categories

# Register your models here.
# class LocationAdmin(admin.ModelAdmin):
#     pass
#
#
# class UserAdmin(admin.ModelAdmin):
#     pass
#
#
# class AdvertAdmin(admin.ModelAdmin):
#     pass
#
#
# class CategoriesAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Location)
admin.site.register(User)
admin.site.register(Advert)
admin.site.register(Categories)