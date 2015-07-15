# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#i18n (just in case)
from django.utils.translation import ugettext_lazy as _

# Logging
import logging
logger = logging.getLogger(__name__)

class PartsmanagementException(Exception):
    """
    Base exceptions for this packages
    """
    logger.error(_("An fatal error has been occurred"))
    pass

class PartsNotFitException(PartsmanagementException):
    """
    Shall be used, when ever a Part is not fitting to another such like cannot be compared
    """
    logger.error(_("Exception: Parts cannot be combined"))
    pass

