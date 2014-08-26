__author__ = 'heddevanderheide'

# Django specific
from django.conf import settings
from django.db import models

# App specific
from networth.managers import NetworthManager
from networth.mixins import NetworthMixin


class NetworthModel(NetworthMixin, models.Model):
    _networth = models.IntegerField(default=getattr(settings, 'NETWORTH_DEFAULT', 0))

    objects = NetworthManager()

    class Meta:
        abstract = True

    def relative_networth(self):
        # returns relative networth (percentual) compared to the
        # highest valued object

        ceiling = self.__class__.objects.ceiling()

        if ceiling == 0:
            return 100
        else:
            if self._networth:
                if self._networth == ceiling:
                    return 100

                return int((float(self._networth) / ceiling) * 100)

            return 0

    def _commit(self, n):
        self._networth = n
        self.save()