# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist

from models import Page


def pages(request):
    pass

def page(request,slug):
    
    try:
        page = Page.activated.get(slug=slug)
    except ObjectDoesNotExist:
        page = None
    
    template = loader.get_template('cms/page.html')
    context = RequestContext(request, {
        'page'  : page,
    })
    return HttpResponse(template.render(context))