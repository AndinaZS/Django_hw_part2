from django.contrib import admin
from ads.models import Advert, Categories

#
# class AdvertAdmin(admin.ModelAdmin):
#     pass
#
#
# class CategoriesAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Advert)
admin.site.register(Categories)