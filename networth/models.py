__author__ = 'heddevanderheide'

# Django specific
from django.conf import settings
from django.db import models

# App specific
from networth.managers import NetworthManager
from networth.mixins import NetworthMixin


class NetworthModel(NetworthMixin, models.Model):
    __networth = models.IntegerField(default=getattr(settings, 'NETWORTH_DEFAULT', 0))

    objects = NetworthManager()

    class Meta:
        abstract = True

    def relative_networth(self):
        # returns relative networth (percentual) compared to the
        # highest valued object

        ceiling = self.__class__.networth_manager.ceiling()

        if self.networth:
            if self.networth == ceiling:
                return 100

            return int((float(self.networth) / ceiling) * 100)

        return 0

    def _commit(self, n):
        self.__networth = n
        self.save()