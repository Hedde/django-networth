__author__ = 'heddevanderheide'

# Django specific
from django.dispatch import Signal

# Notifier when ceiling increases
ceiling_increased = Signal(providing_args=["instance"])