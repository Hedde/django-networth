__author__ = 'heddevanderheide'

# Django specific
from django.db import models

# App specific
from networth.models import NetworthModel


class TestModel(NetworthModel):
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=75, blank=True, null=True)

    class Networth:
        fields = (
            ('first_name', (True, 1)),
            ('last_name', (lambda f: f.startswith('P'), 5)),
        )
