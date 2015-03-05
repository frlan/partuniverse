# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class PartsmanagementException(Exception):
    """
    Base exceptions for this packages
    """
    pass

class PartsNotFitException(PartsmanagementException):
    """
    Shall be used, when ever a Part is not fitting to another such like cannot be compared
    """
    print ('foo')
