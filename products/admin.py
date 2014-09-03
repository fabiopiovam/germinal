# -*- coding: utf-8 -*-

from django.contrib import admin
from products.models import Product, Producer, Segment, Certificate, Country, State, ProductionSys, Photo

class PhotoInline(admin.TabularInline):
    template = 'admin/tabular_image.html'
    model = Photo
    extra = 1
    fields = ['image','main','title']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'producer','owner','available','published')
    list_filter = ['producer__name','segment__title','available','published']
    search_fields = ['title','slug','ingredients','owner__username']
    
    fieldsets = [
        (None,          {'fields': ['title','unit','harvest_from','harvest_until']}),
        (None,          {'fields': ['producer','segment','certificate']}),
        (u"Preço",      {'fields': ['retail_price','wholesale_price']}),
        (u"Detalhes",   {'fields': ['description','characteristics','ingredients','nutrition_facts']}),
        (u"Publicação", {'fields': ['available','published']}),
    ]
    
    inlines = [PhotoInline]
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner_id', None) is None:
            obj.owner_id = request.user.id
        obj.save()


class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name','city','state','responsible','contact','phone','email')
    list_filter = ['state__name','country__name']
    search_fields = ['name','responsible','contact','email','website']
    
    fieldsets = [
        (None,              {'fields': ['name','production_sys']}),
        (u"Localização",    {'fields': ['city','state','country']}),
        (u"Contato",        {'fields': ['responsible','contact','phone','email','website']}),
    ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Segment)
admin.site.register(Certificate)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(ProductionSys)