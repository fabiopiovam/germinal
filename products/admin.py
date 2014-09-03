# -*- coding: utf-8 -*-

from django.contrib import admin
from products.models import Product, Producer, Segment, Certificate, Country, State, ProductionSys, Photo

class PhotoInline(admin.TabularInline):
    template = 'admin/tabular_image.html'
    model = Photo
    extra = 1
    fields = ['image','main','title']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'producer', 'segment', 'owner')
    list_filter = ['producer','segment','available','published']
    search_fields = ['title','slug','owner__username']
    
    fieldsets = [
        (None,          {'fields': ['title','unit','harvest_from','harvest_until']}),
        (None,          {'fields': ['producer','segment','certificate']}),
        (u"Preço",      {'fields': ['retail_price','wholesale_price']}),
        (u"Detalhes",   {'fields': ['description','nutrition_facts']}),
        (u"Publicação", {'fields': ['available','published']}),
    ]
    
    inlines = [PhotoInline]
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner_id', None) is None:
            obj.owner_id = request.user.id
        obj.save()

admin.site.register(Product, ProductAdmin)
admin.site.register(Producer)
admin.site.register(Segment)
admin.site.register(Certificate)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(ProductionSys)