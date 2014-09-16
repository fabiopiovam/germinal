# -*- coding: utf-8 -*-

from django.contrib import admin
from products.models import Product, Producer, Segment, Certificate, Country, State, ProductionSys, Photo
from adminsortable.admin import SortableAdmin, SortableTabularInline
from tags import set_tags
from tags.forms import FormTags

class FormProduct(FormTags):
    class Meta:
        model = Product

class PhotoInline(SortableTabularInline):
    model = Photo
    extra = 1

class ProductAdmin(SortableAdmin):
    list_display = ('title', 'producer','owner','available','published')
    list_filter = ['producer__name','segment__title','available','published']
    search_fields = ['title','slug','ingredients','owner__username']
    filter_horizontal = ('segment','certificate')
    
    fieldsets = [
        (None,          {'fields': ['title','unit','harvest_from','harvest_until']}),
        (None,          {'fields': ['producer','segment','certificate']}),
        (u"Preço",      {'fields': ['retail_price','wholesale_price']}),
        (u"Detalhes",   {'fields': ['description','characteristics','ingredients','nutrition_facts','tags']}),
        (u"Publicação", {'fields': ['available','published']}),
    ]
    
    inlines = [PhotoInline]
    
    form = FormProduct
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner_id', None) is None:
            obj.owner_id = request.user.id
        obj.save()
        
        set_tags(obj, form.cleaned_data['tags'])


class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name','city','state','responsible','contact','phone','email')
    list_filter = ['state__name','country__name']
    search_fields = ['name','responsible','contact','email','website']
    
    fieldsets = [
        (None,              {'fields': ['name','production_sys']}),
        (u"Localização",    {'fields': ['city','state','country']}),
        (u"Contato",        {'fields': ['responsible','contact','phone','email','website']}),
    ]


class SegmentAdmin(admin.ModelAdmin):
    list_display = ('title','slug')
    search_fields = ['title','slug','description']
    fields = ('title','description','image')

admin.site.register(Product, ProductAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Segment, SegmentAdmin)
admin.site.register(Certificate)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(ProductionSys)