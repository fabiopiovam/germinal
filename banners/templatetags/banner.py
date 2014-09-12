from django.template import Library
from django.core.exceptions import ObjectDoesNotExist

from banners.models import Banner

register = Library()

@register.inclusion_tag('banners/banner.html', takes_context=True)
def generate_banner(context, banner=''):
    if not banner:
        return {'banner': '',}
    
    try:
        obj = Banner.activated.get(type=banner)
        range_banner = range(obj.images_set().count())
    except ObjectDoesNotExist:
        obj = None
        range_banner = []
    
    return {'banner': obj, 'range_banner': range_banner, 'MEDIA_URL': context['MEDIA_URL']}