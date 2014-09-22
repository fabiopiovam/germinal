from django.template import Library
from django.core.exceptions import ObjectDoesNotExist

from products.models import Segment

register = Library()

@register.assignment_tag
def get_segments_list():    
    try:
        segments = Segment.objects.all()
    except ObjectDoesNotExist:
        segments = None
    
    return segments