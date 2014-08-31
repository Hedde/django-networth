__author__ = 'heddevanderheide'

# Django specific
from django.dispatch import receiver

# App specific
from networth.signals import ceiling_increased

@receiver(ceiling_increased)
def ceiling_increased_callback(sender, instance, **kwargs):
    print("{} is now the worthiest pizza!".format(instance.name))