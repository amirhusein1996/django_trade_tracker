from django.contrib import admin
from .models import User , UserExtraInformations

class UserModelAdmin(admin.ModelAdmin):
    list_display = 'email' ,


admin.site.register(User , UserModelAdmin)
admin.site.register(UserExtraInformations)

