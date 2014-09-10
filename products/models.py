# -*- coding: utf-8 -*-
import random, glob, os, shutil
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.conf import settings

from ckeditor.fields import RichTextField
from easy_thumbnails.fields import ThumbnailerImageField
from adminsortable.models import Sortable
from adminsortable.fields import SortableForeignKey

month_choices = (
    (1, u'Janeiro'), (2, u'Fevereiro'), (3, u'Março'),
    (4, u'Abril'), (5, u'Maio'), (6, u'Junho'), 
    (7, u'Julho'), (8, u'Agosto'), (9, u'Setembro'),
    (10, u'Outubro'), (11, u'Novembro'), (12, u'Dezembro'),
)

class Country(models.Model):
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = u"País"
        verbose_name_plural = u"Países"
    
    name = models.CharField(u'País', max_length=80)
    code = models.CharField(u'Código', max_length=4)

class State(models.Model):
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = u"UF"
    
    country = models.ForeignKey(Country, verbose_name=u"País")
    name = models.CharField(u'Estado', max_length=80)
    acronym = models.CharField(u'Sigla', max_length=4)

class ProductionSys(models.Model):
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = u"Sistema de Produção"
    
    name = models.CharField(u'Nome', max_length=80)

class Producer(models.Model):
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = u"produtor"
        verbose_name_plural = u"produtores"
    
    production_sys = models.ManyToManyField(ProductionSys, null=True, blank=True, verbose_name=u"Sistema de Produção")
    state = models.ForeignKey(State, verbose_name=u"UF")
    country = models.ForeignKey(Country, verbose_name=u"País")
    name = models.CharField(u'Produtor', max_length=160)
    responsible = models.CharField(u'Responsável', null=True, blank=True, max_length=160)
    contact = models.CharField(u'Contato', null=True, blank=True, max_length=160)
    city =  models.CharField(u'Cidade', max_length=160)
    email =  models.EmailField(u'E-mail', null=True, blank=True, max_length=100)
    phone =  models.CharField(u'Telefone', null=True, blank=True, max_length=100)
    website =  models.CharField(u'Website', null=True, blank=True, max_length=100)
    
class Segment(models.Model):
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        verbose_name = u"segmento"
    
    title = models.CharField(u'Segmento', max_length=160)

class Certificate(models.Model):
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        verbose_name = u"certificado"
    
    title = models.CharField(u'Título', max_length=160)

class Photo(Sortable):
    class Meta(Sortable.Meta):
        verbose_name = u"foto"
    
    def save(self):
        if self.image:
            if self.id:
                obj_photo = Photo.objects.get(id=self.id)
                if self.image not in [obj_photo.image]:
                    for fl in glob.glob("%s/%s*" % (settings.MEDIA_ROOT,obj_photo.image)):
                        os.remove(fl)
            
            super(Photo, self).save()
    
    def delete(self):
        obj_photo = Photo.objects.get(id=self.id)
        super(Photo, self).delete()
        for fl in glob.glob("%s/%s*" % (settings.MEDIA_ROOT,obj_photo.image)):
            os.remove(fl)
    
    def get_upload_to_image(self, filename):
        ext = filename[-3:].lower()
        if ext == 'peg': ext='jpeg'        
        return 'products/%s/%s_%s.%s' % (self.products.slug, datetime.now().strftime('%Y%m%d%H%M%S'), str(random.randint(00000,99999)), ext)
    
    def __unicode__(self):
        return u'%s' % self.image
    
    products = SortableForeignKey('Product')
    image = ThumbnailerImageField(u'Imagem', upload_to = get_upload_to_image, resize_source=dict(size=(800, 600), sharpen=False, crop="scale"))
    title = models.CharField(u'Título', max_length=100, blank=True, null=True)

class ProductActivatedManager(models.Manager):
    def get_queryset(self):
        return super(ProductActivatedManager, self).get_queryset().filter(published=True).order_by('-updated_at')

class Product(Sortable):
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta(Sortable.Meta):
        verbose_name = u"produto"
    
    def save(self, *args, **kwargs):
        if not self.id:
            super(Product, self).save(*args, **kwargs)
            self.slug = slugify(str(self.id) + ' ' + self.title)
        super(Product, self).save(*args, **kwargs)
        
    def delete(self):
        slug = self.slug
        super(Product, self).delete()
        
        dir = '%s/products/%s' % (settings.MEDIA_ROOT, slug)
        
        if os.path.exists(dir):
            shutil.rmtree(dir)
    
    def get_absolute_url(self):
        return reverse('products.views.details', kwargs={'slug': self.slug})
    
    def main_photo_set(self):
        photo = self.photo_set.order_by('order')
        return photo[0] if photo else None
    
    owner = models.ForeignKey(User, verbose_name=u"Usuário")
    producer = models.ForeignKey(Producer, verbose_name=u"Produtor")
    segment = models.ManyToManyField(Segment, verbose_name=u"Segmento", null=True, blank=True)
    certificate = models.ManyToManyField(Certificate, null=True, blank=True, verbose_name=u"Certificado")
    
    title = models.CharField(u'Título', max_length=160)
    slug = models.SlugField(max_length=200)
    unit = models.CharField(u'Unidade', max_length=10)
    harvest_from = models.IntegerField(u'Safra (início)', null=True, blank=True, choices=month_choices)
    harvest_until = models.IntegerField(u'Safra  (fim)', null=True, blank=True, choices=month_choices)
    retail_price = models.DecimalField(u'Varejo R$', max_digits=6, decimal_places=2, blank=True, null=True)
    wholesale_price = models.DecimalField(u'Atacado R$', max_digits=6, decimal_places=2, blank=True, null=True)
    description =  RichTextField(verbose_name=u'Descrição', null=True, blank=True)
    characteristics =  RichTextField(verbose_name=u'Características', null=True, blank=True)
    ingredients =  RichTextField(verbose_name=u'Ingredientes', null=True, blank=True)
    nutrition_facts = RichTextField(verbose_name=u'Informações nutricionais', null=True, blank=True)
    
    published = models.BooleanField(u'Publicado', default=True)
    available = models.BooleanField(u'Disponível', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    u''' Managers '''
    objects     = models.Manager()
    activated   = ProductActivatedManager()