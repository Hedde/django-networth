__author__ = 'heddevanderheide'

# Django specific
from django.db import models
from django.db.models import Max
from django.db.models.query import QuerySet


class NetworthQuerySet(QuerySet):
    def ceiling(self):
        return self.aggregate(Max('_networth'))['_networth__max']


class NetworthManager(models.Manager):
    def get_queryset(self):
        return NetworthQuerySet(self.model, using=self._db)