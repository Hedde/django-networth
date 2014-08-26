__author__ = 'heddevanderheide'

# Django specific
from django.db import models
from django.db.models import Max


class NetworthManager(models.Manager):
    def ceiling(self):
        return self.get_queryset().aggregate(Max('_networth'))['_networth__max']