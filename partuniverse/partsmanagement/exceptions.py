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


class CircleDetectedException(PartsmanagementException):
    """
    Used in case of a chained list is showing some circles
    """
    def __init__(self, error):
        logger.error(_(u"Circle detected: %s" % error))


class StorageItemBelowZeroException(PartsmanagementException):
    """
    Used in case of trying to set a StorageItem with an negative amount
    of items
    """
    def __init__(self, error):
        logger.error(_(u("Amount of items inside a storage cannot be under 0:",
            "%s") % error))
