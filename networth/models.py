__author__ = 'heddevanderheide'

# Django specific
from django.conf import settings
from django.db import models

# App specific
from networth.managers import NetworthManager
from networth.mixins import NetworthMixin
from networth.signals import ceiling_increased, ceiling_decreased


class NetworthModel(NetworthMixin, models.Model):
    _networth = models.IntegerField(default=getattr(settings, 'NETWORTH_DEFAULT', 1))
    _relative_networth = models.IntegerField(default=0)

    objects = NetworthManager()

    class Meta:
        abstract = True

    def get_default_networth(self):
        return getattr(settings, 'NETWORTH_DEFAULT', 1)

    def networth(self, realtime=False, commit=False):
        if realtime:
            qs = self.__class__.objects.all()

            ceiling = qs.ceiling()
            ceiling_minus_self = qs.exclude(pk=self.pk).ceiling()

            h, n = self._networth, self.__networth(commit=commit)

            if n > h:
                if n > ceiling:
                    ceiling_increased.send(
                        sender=self.__class__,
                        instance=self
                    )
            elif h > n > ceiling_minus_self:
                ceiling_decreased.send(
                    sender=self.__class__,
                    instance=self
                )

            return n
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