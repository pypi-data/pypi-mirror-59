# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import sqliteschema
import tabledata

from ._null_logger import NullLogger


def _disable_logger(l):
    try:
        l.disable()
    except AttributeError:
        l.disabled = True  # to support Logbook<1.0.0


try:
    import logbook

    logger = logbook.Logger("SimpleSQLie")
    _disable_logger(logger)
    LOGBOOK_INSTALLED = True
except ImportError:
    logger = NullLogger()
    LOGBOOK_INSTALLED = False


def set_logger(is_enable):
    if not LOGBOOK_INSTALLED:
        return

    if is_enable != logger.disabled:
        # logger setting have not changed
        return

    if is_enable:
        try:
            logger.enable()
        except AttributeError:
            logger.disabled = False  # to support Logbook<1.0.0
    else:
        _disable_logger(logger)

    tabledata.set_logger(is_enable)
    sqliteschema.set_logger(is_enable)
    try:
        import pytablereader

        pytablereader.set_logger(is_enable)
    except ImportError:
        pass


def set_log_level(log_level):
    """
    Set logging level of this module. Using
    `logbook <https://logbook.readthedocs.io/en/stable/>`__ module for logging.

    :param int log_level:
        One of the log level of
        `logbook <https://logbook.readthedocs.io/en/stable/api/base.html>`__.
        Disabled logging if ``log_level`` is ``logbook.NOTSET``.
    :raises LookupError: If ``log_level`` is an invalid value.
    """

    if not LOGBOOK_INSTALLED:
        return

    # validate log level
    logbook.get_level_name(log_level)

    if log_level == logger.level:
        return

    if log_level == logbook.NOTSET:
        set_logger(is_enable=False)
    else:
        set_logger(is_enable=True)

    logger.level = log_level
    tabledata.set_log_level(log_level)
    sqliteschema.set_log_level(log_level)
    try:
        import pytablereader

        pytablereader.set_log_level(log_level)
    except ImportError:
        pass
