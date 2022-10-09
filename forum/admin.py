from django.contrib import admin

from forum.models import ThemeForum


class ForumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(ThemeForum, ForumAdmin)
