# -*- coding: utf-8 -*-

from django.contrib import admin
from cms.models import Category, Page

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ['title', 'slug']
    fields = ('title',)

class PageAdmin(admin.ModelAdmin):
    list_display = ('title','published')
    search_fields = ['title','slug']
    list_filter = ['category__title','published']
    fields = ('title','content','category','published')
    filter_horizontal = ('category',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)