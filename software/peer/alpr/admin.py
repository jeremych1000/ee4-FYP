from django.contrib import admin
from . import models


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(CustomModelAdmin, self).__init__(model, admin_site)

class videos(CustomModelAdmin):
    pass

admin.site.register(models.videos, videos)