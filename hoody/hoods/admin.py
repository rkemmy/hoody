from django.contrib import admin

from . import models


class HoodMemberInline(admin.TabularInline):
    model = models.HoodMember

admin.site.register(models.Hood)