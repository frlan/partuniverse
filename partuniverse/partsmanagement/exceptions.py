# -*- coding: utf-8 -*-

import logging
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class PartsmanagementException(Exception):
    """
    Base exceptions for this packages
    """

    def __init__(self, error):
        super(PartsmanagementException, self).__init__(error)
        logger.error(_("An fatal error has been occurred: %s" % error))


class PartsNotFitException(PartsmanagementException):
    """
    Shall be used, when ever a Part is not fitting to another such like cannot be compared
    """

    def __init__(self, error):
        super(PartsNotFitException, self).__init__(error)
        logger.error(_("Exception: Parts cannot be combined: %s" % error))


class CircleDetectedException(PartsmanagementException):
    """
    Used in case of a chained list is showing some circles
    """

    def __init__(self, error):
        super(CircleDetectedException, self).__init__(error)
        logger.error(_("Circle detected: %s" % error))


class StorageItemBelowZeroException(PartsmanagementException):
    """
    Used in case of trying to set a StorageItem with an negative amount
    of items
    """

    def __init__(self, error):
        super(StorageItemBelowZeroException, self).__init__(error)
        logger.error(
            _(("Amount of items inside a storage cannot be under 0:", "%s") % error)
        )


class StorageItemIsTheSameException(PartsmanagementException):
    """
    Used in case of trying to merge one and the smae storage item"
    """

    def __init__(self, error):
        super(StorageItemIsTheSameException, self).__init__(error)
        logger.error(_("Storage Items are idendical: %s" % error))


class TransactionAllreadyRevertedException(PartsmanagementException):
    """
    Used in case of trying to set revert an already marked a reverted transaction
    """

    def __init__(self, error):
        super(TransactionAllreadyRevertedException, self).__init__(error)
        logger.error(_("Cannot revert Transaction: %s" % error))
