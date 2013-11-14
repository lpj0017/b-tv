# coding=UTF-8
from models import *
from django.contrib import admin

class VideoURLAdmin(admin.ModelAdmin):
    list_filter = ('is_saved',)
    list_display = ('url', 'is_saved',)
    list_editable = ('is_saved',)

#admin.site.register(Project)
admin.site.register(Video)
admin.site.register(Part)
admin.site.register(Topic)
admin.site.register(VideoURL,VideoURLAdmin)

