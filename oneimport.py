"""
Module 'oneimport' makes it easy to import most common libraries like this:

    from oneimport import *

The above line is roughly equivalent to:

    import os, sys, re, time, datetime, collections, logging
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s {arg0}[%(process)d] [%(levelname)s] %(message)s'.format(arg0=os.path.basename(sys.argv[0]))
    logger = logging.getLogger(__name__)

Default logging level is DEBUG if the output is to a TTY, INFO otherwise.

Note that even if you use oneimport, you can override the logging setup by adding a handler to the root logger before
logging anything.

"""

import os
import sys
import re
import time
import datetime
import collections
import logging


class _FakeLogger(object):
    """
    This makes the logger object work as expected unless it got redefined by the importing module.

    There is one side effect: the logging setup is not done until after the first call to logger from
    the importer. Any sub-module that uses logging before that will not have any setup done. To avoid
    this, use the logger object first.

    You can force initialize the logger like this:
        logger.info  # No parentheses, just the act of looking at logger method will initialize the logger

    This also means that if logging is not used, it's never initialized.

    Logging setup is only done if the root logger doesn't already have a handler, that way,
    calling basicConfig or setting up a handler for the root logger will disable the defaults in here.
    """
    _logger = None

    def __init__(self, name):
        self._name = name

    def __getattr__(self, item):
        if self._logger is None:
            self._setLogging()
        self.__dict__[item] = getattr(self._logger, item)
        return self.__dict__[item]

    def _setLogging(self):
        self._logger = logging.getLogger(self._name)
        if len(logging.root.handlers) == 0:
            if sys.stdout.isatty():
                logging.root.setLevel(logging.DEBUG)
            else:
                logging.root.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s {arg0}[%(process)d] [%(levelname)s] %(message)s'.format(
                arg0=os.path.basename(sys.argv[0])))
            handler.setFormatter(formatter)
            logging.root.addHandler(handler)


logger = _FakeLogger(sys._getframe(1).f_globals.get('__name__'))
