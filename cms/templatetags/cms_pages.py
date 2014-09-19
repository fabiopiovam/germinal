from django.template import Library
from django.core.exceptions import ObjectDoesNotExist

from cms.models import Category, Page

register = Library()

@register.inclusion_tag('cms/list_pages.html')
def list_pages(category=''):
    
    try:
        if not category:
            pages = Page.activated.all()
        else:
            pages = Page.activated.filter(category__slug=category)
        
    except ObjectDoesNotExist:
        pages = None
    
    return {'pages': pages,}