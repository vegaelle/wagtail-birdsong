from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.utils import camelcase_to_underscore

from .blocks import DefaultBlocks
from .backends import BaseEmailBackend


class BaseEmail(models.Model):
    subject = models.TextField()
    sent_date = models.DateTimeField(blank=True, null=True)

    panels = [
        FieldPanel('subject'),
    ]

    def get_template(self, request):
        return "%s/mail/%s.html" % (self._meta.app_label, camelcase_to_underscore(self.__class__.__name__))
    
    def get_backend(self):
        return BaseEmailBackend

    class Meta:
        abstract = True


class Contact(models.Model):
    first_name = models.TextField() 
    email = models.EmailField()
