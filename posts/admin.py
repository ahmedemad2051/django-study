from django.contrib import admin
from .models import Post


class postAdmin(admin.ModelAdmin):
    list_display = ['id','__str__','timestamp']
    list_filter=['timestamp']
    search_fields = ['title']
    list_display_links = ['__str__']
admin.site.register(Post,postAdmin)
