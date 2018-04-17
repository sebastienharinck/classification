from django.contrib import admin

from .models import Image, Vote


class HashAdmin(admin.ModelAdmin):
    readonly_fields = ('hash',)


class CreateAtAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )
    list_display = ['image', 'user', 'label', 'choice']
    search_fields = ('label__name', 'image__hash', 'user__username')


admin.site.register(Image, HashAdmin)
admin.site.register(Vote, CreateAtAdmin)
