# -*- coding: utf-8 -*-


from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FAQConfig(AppConfig):
    name = 'aparnik.contrib.faq'
    verbose_name = _('Frequently Asked Questions')
