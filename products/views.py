# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from models import Product
from banners.models import Banner

def index(request):
    product_list        = Product.activated.all()[:8]
    banner_principal    = Banner.activated.get(type='principal')
    
    template = loader.get_template('products/index.html')
    context = RequestContext(request, {
        'product_list'  : product_list,
        'banner_principal'  : banner_principal,
    })
    return HttpResponse(template.render(context))


def details(request, slug):
    try:
        product = Product.activated.get(slug=slug)
    except ObjectDoesNotExist:
        product = None
    
    try:
        http_referer = request.environ['HTTP_REFERER']
    except KeyError:
        http_referer = '/'
    
    template = loader.get_template('products/details.html')
    context = RequestContext(request, {
        'product'   : product,
        'http_referer' : http_referer,
    })
    return HttpResponse(template.render(context))