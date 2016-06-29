from django.contrib import admin
from .models import Post


class postAdmin(admin.ModelAdmin):
    list_display = ['id','__unicode__','timestamp']
    list_filter=['timestamp']
    search_fields = ['title']
admin.site.register(Post,postAdmin)
