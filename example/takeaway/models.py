__author__ = 'heddevanderheide'

# Django specific
from django.db import models
from django.utils.translation import ugettext_lazy as _

# App specific
from networth.models import NetworthModel


class Topping(models.Model):
    name = models.CharField(max_length=140, blank=True, null=True)

    class Meta:
        verbose_name = _(u"Topping")
        verbose_name_plural = _(u"Toppings")

    def __unicode__(self):
        return self.name


class Pizza(NetworthModel):
    name = models.CharField(max_length=140, blank=True, null=True)
    toppings = models.ManyToManyField('takeaway.Topping', null=True)

    class Meta:
        verbose_name = _(u"Pizza")
        verbose_name_plural = _(u"Pizze")

    class Networth:
        fields = (
            ('name', (True, 0)),
            ('toppings', (lambda m: m.count(), 'result'))
        )

    def __unicode__(self):
        return self.name