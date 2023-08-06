# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import abc

import dataproperty
import six

from ._null_logger import NullLogookLogger


def _disable_logger(l):
    try:
        l.disable()
    except AttributeError:
        l.disabled = True  # to support Logbook<1.0.0


try:
    import logbook

    logger = logbook.Logger("pytablereader")
    _disable_logger(logger)
    LOGBOOK_INSTALLED = True
except ImportError:
    logger = NullLogookLogger()
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

    dataproperty.set_logger(is_enable)

    try:
        import simplesqlite

        simplesqlite.set_logger(is_enable)
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
    dataproperty.set_log_level(log_level)

    try:
        import simplesqlite

        simplesqlite.set_log_level(log_level)
    except ImportError:
        pass


def typehints_to_str(type_hints):
    return ", ".join([type_hint.__name__ if type_hint else "none" for type_hint in type_hints])


@six.add_metaclass(abc.ABCMeta)
class LoggerInterface(object):
    @abc.abstractmethod
    def logging_load(self):  # pragma: no cover
        pass


class BaseLogger(LoggerInterface):
    def __init__(self, loader):
        self._loader = loader

    def logging_load(self):
        logger.debug(self._get_load_message())

    def logging_table(self, table_data):
        logger.debug("loaded tabledata: {}".format(table_data))

    @abc.abstractmethod
    def _get_load_message(self):
        pass


class NullLogger(BaseLogger):
    def logging_load(self):
        pass

    def logging_table(self, table_data):
        pass

    def _get_load_message(self):
        return ""


class FileSourceLogger(BaseLogger):
    def _get_load_message(self):
        message = "loading {:s}: format={:s}, path={}".format(
            self._loader.source_type, self._loader.format_name, self._loader.source
        )

        try:
            message += ", encoding={}".format(self._loader.encoding)
        except AttributeError:
            pass

        if self._loader.type_hints:
            message += ", type-hints=({})".format(typehints_to_str(self._loader.type_hints))

        return message


class TextSourceLogger(BaseLogger):
    def _get_load_message(self):
        message = "loading {:s}: format={:s}".format(
            self._loader.source_type, self._loader.format_name
        )

        try:
            message += ", len={}".format(len(self._loader.source))
        except TypeError:
            pass

        try:
            message += ", encoding={}".format(self._loader.encoding)
        except AttributeError:
            pass

        if self._loader.type_hints:
            message += ", type-hints=({})".format(typehints_to_str(self._loader.type_hints))

        return message
