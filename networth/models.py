__author__ = 'heddevanderheide'

# Django specific
from django.conf import settings
from django.db import models

# App specific
from networth.managers import NetworthManager
from networth.mixins import NetworthMixin


class NetworthModel(NetworthMixin, models.Model):
    _networth = models.IntegerField(default=getattr(settings, 'NETWORTH_DEFAULT', 0))
    _relative_networth = models.IntegerField(default=0)

    objects = NetworthManager()

    class Meta:
        abstract = True

    def relative_networth(self, commit=False):
        return self.__relative_networth(commit=commit)

    def __relative_networth(self, commit=False):
        # returns relative networth (percentual) compared to the
        # highest valued object

        ceiling = self.__class__.objects.ceiling()

        if ceiling == 0:
            n = 100
        else:
            if self._networth:
                if self._networth == ceiling:
                    n = 100
                else:
                    n = int((float(self._networth) / ceiling) * 100)
            else:
                n = 0

        if commit:
            self._commit('_relative_networth', n)

        return n

    def _commit(self, field, value):
        setattr(self, field, value)
        self.save()