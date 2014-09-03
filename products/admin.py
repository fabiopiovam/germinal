from django.contrib import admin
from products.models import Product, Producer, Segment, Certificate, Country, State, ProductionSys

admin.site.register(Product)
admin.site.register(Producer)
admin.site.register(Segment)
admin.site.register(Certificate)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(ProductionSys)