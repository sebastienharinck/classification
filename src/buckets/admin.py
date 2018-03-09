from django.contrib import admin
from .models import Bucket, Label


admin.site.register(Bucket)
admin.site.register(Label)
