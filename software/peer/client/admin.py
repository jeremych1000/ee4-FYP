from django.contrib import admin
from . import models


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(CustomModelAdmin, self).__init__(model, admin_site)

class bootstrap(CustomModelAdmin):
    pass
class plates(CustomModelAdmin):
    pass
class peer_list(CustomModelAdmin):
    pass
class violations(CustomModelAdmin):
    pass

admin.site.register(models.bootstrap, bootstrap)
admin.site.register(models.plates, plates)
admin.site.register(models.peer_list, peer_list)
admin.site.register(models.violations, violations)