# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


class RunoneAdmin(admin.ModelAdmin):
    model = Runone
    list_display = ('name', 'user', 'created',)
    prepopulated_fields = {'slug': ('name',)}



class UploadAdmin(admin.ModelAdmin):
    list_display = ('runshow',)
    list_display_links = ('runshow',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'body')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Runone, RunoneAdmin)
admin.site.register(Upload, UploadAdmin)
