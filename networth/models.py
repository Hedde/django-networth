__author__ = 'heddevanderheide'

# Django specific
from django.db import models
from django.db.models import Model


class NetworthModel(Model):
    networth = models.IntegerField()

    class Meta:
        abstract = True

    def _networth(self, commit=False):
        n = 0

        for field in self.__class__.Networth.fields:
            f, values = field

            v = getattr(self, f)

            if callable(values[0]):
                if values[1] == 'result':
                    n += values[0](v)
                elif callable(values[1]):
                    n += values[1](values[0](v))
                else:
                    print f
                    n += values[1]
            else:
                if type(values[0]) == bool and bool(v) == values[0]:
                    n += values[1]
                elif v == values[0]:
                    n += values[1]

        if commit:
            self.networth = n
            self.save()

        return n