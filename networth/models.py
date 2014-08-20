__author__ = 'heddevanderheide'

# Django specific
from django.db import models
from django.db.models import Model


class NetworthModel(Model):
    """
    Implementation example

    class Object(NetworthModel):
        first_name = models.CharField(max_length=25)
        last_name = models.CharField(max_length=75, blank=True, null=True)

        tags = TaggableManager(through=TaggedItem, blank=True)

        class Networth:
            fields = (
                ('first_name', (True, 1)),
                ('last_name', (lambda f: f.startswith('P'), 5)),
                ('tags', (lambda f: f.count(), 'result'))
            )

        Consider the following pseudo instances:

        ('Pete',).networth() > 1
        ('Pete', 'James').networth() > 1
        ('Pete', 'Philly').networth() > 6

        A more complex example:

        ('Pete', 'Philly', <TagManager>).networth() > 0

        In this example 'result' uses the outcome of the function as the net result
        As we have not added any tags to Pete yet, the count() will be zero.


        Declaring your own Networh logic:

        from networth.models import NetworthModel as BaseNetworthModel

        class NetworthModel(BaseNetworthModel):
            def networth(self):
                return super(NetworthModel, self).networth()

    """
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
                else:
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