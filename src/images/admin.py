from django.contrib import admin

from .models import Image, Tag, Vote


class CreateAtAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )


admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Vote, CreateAtAdmin)
