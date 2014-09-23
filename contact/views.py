# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.mail import mail_managers
from django.conf import settings

from forms import ContactForm

def contact(request):
    
    mail_sent = None
    
    if request.method == 'POST':
        
        form = ContactForm(request.POST)
        if form.is_valid():
            url     = request.build_absolute_uri()
            name    = form.cleaned_data['name']
            email   = form.cleaned_data['email']
            phone   = form.cleaned_data['phone']
            subject = u'Contato de ' + name
            message = form.cleaned_data['message']
            message = u'Mensagem enviada por %s <%s> %s \n\n%s \n\n\nMensagem enviada através da página:\n%s' % (name, email, phone, message, url)
            
            try:
                mail_managers(subject, message, fail_silently = False)
                mail_sent = True
            except Exception as e:
                mail_sent = False
                if settings.DEBUG:
                    raise # reraises the exception
    else:
        form = ContactForm()
    
    template = loader.get_template('contact/contact.html')
    context = RequestContext(request, {
        'form'      : form,
        'mail_sent' : mail_sent,
    })
    return HttpResponse(template.render(context))