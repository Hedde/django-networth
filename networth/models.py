__author__ = 'heddevanderheide'

# Django specific
from django.db import models
from django.db.models import Model

# App specific
from networth.managers import NetworthManager


class NetworthMixin(object):
    def _networth(self, commit=False):
        n = 0

        for field in self.__class__.Networth.fields:
            f, values = field

            v = getattr(self, f)

            definition, points = values
            definition_is_callable, points_is_callable = callable(definition), callable(points)

            if definition_is_callable:

                if values[1] == 'result':
                    n += definition(v)

                elif points_is_callable:
                    n += points(definition(v))

                else:
                    n += points

            else:

                if type(definition) == bool:
                    if points_is_callable:
                        n += points(1 if bool(v) == definition else 0)
                    else:
                        n += points

                elif points == 'result':
                    n += v

                elif points_is_callable:
                    n += points(v)

                else:
                    n += points

        if commit:
            self._commit(n)

        return n

    def _commit(self, n):
        raise NotImplementedError


class NetworthModel(NetworthMixin, Model):
    networth = models.IntegerField()

    networth_manager = NetworthManager()

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
        self.networth = n
        self.save()