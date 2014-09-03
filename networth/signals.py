__author__ = 'heddevanderheide'

# Django specific
from django.dispatch.dispatcher import Signal

# Notifier when ceiling increases
ceiling_increased = Signal(providing_args=["instance"])

# Notifier when ceiling decreases
ceiling_decreased = Signal(providing_args=["instance"])