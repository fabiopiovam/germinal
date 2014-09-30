import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib.sites.models import Site
from django.template import Context, TemplateDoesNotExist

from newsletter.views import UpdateSubscriptionViev
from newsletter.models import Message, EmailMultiAlternatives

class UpdateSubscriptionViev(UpdateSubscriptionViev):
    
    def send_welcome_message(self, slug):
        
        message = Message.objects.get(slug = slug)
        
        (subject_template, text_template, html_template) = \
            message.newsletter.get_templates('message')
        
        variable_dict = {
            'subscription': self.subscription,
            'site': Site.objects.get_current(),
            'message': message,
            'newsletter': message.newsletter,
            'date': self.subscription.subscribe_date,
            'STATIC_URL': settings.STATIC_URL,
            'MEDIA_URL': settings.MEDIA_URL
        }
        
        unescaped_context = Context(variable_dict, autoescape=False)
        
        subject = subject_template.render(unescaped_context).strip()
        text = text_template.render(unescaped_context)
        
        message = EmailMultiAlternatives(
            subject, text,
            from_email=message.newsletter.get_sender(),
            to=[self.subscription.email]
        )
        
        if html_template:
            escaped_context = Context(variable_dict)

            message.attach_alternative(
                html_template.render(escaped_context), "text/html"
            )
        
        try:
            logger.debug(
                u'Submitting Welcome message after confirmed inscription to: %s.',
                self.subscription
            )

            message.send()

        except Exception, e:
            # TODO: Test coverage for this branch.
            logger.error(
                u'Message %(subscription)s failed '
                         u'with error: %(error)s',
                {'subscription': self.subscription,
                 'error': e}
            )
    
    def form_valid(self, form):
        obj = super(UpdateSubscriptionViev, self).form_valid(form)
        
        self.send_welcome_message("bem-vindxs")
        
        return obj