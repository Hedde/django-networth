__author__ = 'heddevanderheide'

# Django specific
from django.dispatch import receiver

# App specific
from networth.signals import ceiling_increased, ceiling_decreased


@receiver(ceiling_increased)
def ceiling_increased_callback(sender, instance, **kwargs):
    print("{} is now even more populair!".format(instance.name))


@receiver(ceiling_decreased)
def ceiling_decreased_callback(sender, instance, **kwargs):
    print("{} is now less populair!".format(instance.name))