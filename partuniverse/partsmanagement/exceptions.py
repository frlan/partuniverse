# -*- coding: utf-8 -*-

# i18n (just in case)
from django.utils.translation import ugettext_lazy as _

# Logging
import logging
logger = logging.getLogger(__name__)


class PartsmanagementException(Exception):
    """
    Base exceptions for this packages
    """
    def __init__(self, error):
        logger.error(_(u"An fatal error has been occurred: %s" % error))


class PartsNotFitException(PartsmanagementException):
    """
    Shall be used, when ever a Part is not fitting to another such like cannot be compared
    """
    def __init__(self, error):
        logger.error(_(u"Exception: Parts cannot be combined: %s" % error))
