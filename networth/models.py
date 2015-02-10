__author__ = 'heddevanderheide'

# Django specific
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

# App specific
from networth.managers import NetworthManager
from networth.mixins import NetworthMixin


class NetworthModel(NetworthMixin, models.Model):
    _networth = models.IntegerField(verbose_name=_("Networth"),
                                    default=getattr(settings, 'NETWORTH_DEFAULT', 1))
    _relative_networth = models.IntegerField(verbose_name=_("Relative networth"),
                                             default=0)

    objects = NetworthManager()

    class Meta:
        abstract = True

    def get_default_networth(self):
        return getattr(settings, 'NETWORTH_DEFAULT', 1)

    def networth(self, realtime=False, commit=False):
        if realtime:
            return self.__networth(commit=commit)
        return self._networth

    def relative_networth(self, realtime=False, commit=False):
        if realtime:
            return self.__relative_networth(commit=commit)
        return self._relative_networth

    def __networth(self, commit=False):
        return self._NetworthMixin__networth(commit=commit)

    def __relative_networth(self, commit=False):
        # returns relative networth (percentual) compared to the
        # highest valued object

        ceiling = self.__class__.objects.exclude(pk=self.pk).ceiling()

        if ceiling == 1:
            n = 100
        else:
            if self._networth == ceiling:
                n = 100
            else:
                n = int((float(self._networth)) / ceiling * 100)

                if n > 100:
                    n = 100

        if commit:
            self._commit('_relative_networth', n)

        return n

    def _commit(self, field, value):
        setattr(self, field, value)
        self.save()