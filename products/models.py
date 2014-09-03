# -*- coding: utf-8 -*-

from django.template.defaultfilters import slugify

from django.db import models
from redactor.fields import RedactorField

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
    
    name = models.CharField(u'Nome', max_length=80)
    code = models.CharField(u'Código', max_length=4)

class State(models.Model):
    def __unicode__(self):
        return u'%s' % self.name
    
    class Meta:
        verbose_name = u"UF"
    
    country = models.ForeignKey(Country, verbose_name=u"País")
    name = models.CharField(u'Nome', max_length=80)
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
    name = models.CharField(u'Nome', max_length=160)
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
    
    title = models.CharField(u'Título', max_length=160)

class Certificate(models.Model):
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        verbose_name = u"certificado"
    
    title = models.CharField(u'Título', max_length=160)

class Product(models.Model):
    def __unicode__(self):
        return u'%s' % self.title
    
    class Meta:
        verbose_name = u"produto"
    
    def save(self, *args, **kwargs):
        if not self.id:
            super(Product, self).save(*args, **kwargs)
            self.slug = slugify(str(self.id) + ' ' + self.title)
        super(Product, self).save(*args, **kwargs)
    
    producer = models.ForeignKey(Producer, verbose_name=u"Produtor")
    segment = models.ForeignKey(Segment, verbose_name=u"Segmento")
    certificate = models.ManyToManyField(Certificate, null=True, blank=True, verbose_name=u"Certificado")
    
    title = models.CharField(u'Título', max_length=160)
    slug = models.SlugField(max_length=200)
    unit = models.CharField(u'Unidade', max_length=10)
    harvest_from = models.IntegerField(u'Safra', null=True, blank=True, choices=month_choices)
    harvest_until = models.IntegerField(u'', null=True, blank=True, choices=month_choices)
    retail_price = models.DecimalField(u'Varejo R$', max_digits=6, decimal_places=2, blank=True, null=True)
    wholesale_price = models.DecimalField(u'Atacado R$', max_digits=6, decimal_places=2, blank=True, null=True)
    description =  RedactorField(verbose_name=u'Descrição', allow_file_upload=False, allow_image_upload=False, null=True, blank=True)
    nutrition_facts = RedactorField(verbose_name=u'Informações nutricionais', allow_file_upload=False, allow_image_upload=False, null=True, blank=True)
    