#!/usr/bin python
# coding:utf-8
# Created by yubiao.luo at 2020/9/10
import logging
import sys
import os
import traceback
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler


def getTraceback(n=4):
    extype, exval, exstack = sys.exc_info()
    ss = traceback.format_exception(extype, exval, exstack)
    lines = []
    for s1 in ss:
        s2 = s1.split('\n')
        for s3 in s2:
            s4 = s3.strip()
            if len(s4) > 0:
                lines.append(s4)
            # end if
        # end for
    # end for
    return " ==> ".join(lines[-n:])


class Logger(object):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTEST = logging.NOTSET

    logLevel = logging.INFO

    commonLogLevel = logging.INFO

    consoleLogHandler = logging.StreamHandler(sys.stderr)
    RotatingFileHandler = None

    contextLevel = logging.INFO
    # currentContext = ContextVar('currentContext', default={})

    contextText = ContextVar('contextText', default='')

    defaultFormater = "%(asctime)s||pid=%(process)d||tid=%(thread)d||level=%(levelname)s||%(message)s"

    def __init__(self, module=None, level=None):
        self.module = module
        self.logLevel = level or self.commonLogLevel

    @classmethod
    def resetContext(cls):
        # cls.currentContext.set({})
        cls.contextText.set('')

    @classmethod
    def setup(cls, level=logging.INFO, logFile=None):
        cls.commonLogLevel = level

        formatter = logging.Formatter(fmt=cls.defaultFormater)
        cls.consoleLogHandler.setFormatter(formatter)

        cls.RotatingFileHandler = RotatingFileHandler(filename=logFile)
        cls.RotatingFileHandler.setFormatter(formatter)

        cls.resetContext()

    @staticmethod
    def getLogger(name=None, level=None):
        return Logger(name, level)

    def format_msg(self, msg, *args, **kw):
        frame = sys._getframe(3)
        filename = os.path.normpath(frame.f_code.co_filename)
        line_no = frame.f_lineno
        _context = Logger.contextText.get('')
        prefix = "file={}:{}".format(filename, line_no)
        suffix = '||'.join(['{k}={v}'.format(k=k, v=v) for k, v in kw.items()])

        if msg:
            msg = msg % args

        if _context:
            prefix += '||' + _context

        if prefix:
            msg = prefix + '||' + msg

        if suffix:
            msg += '||' + suffix
        return msg

    def log_msg(self, level, msg=None, *args, **kw):
        try:
            msg = self.format_msg(msg, *args, **kw)
            record = logging.LogRecord(self.module, level, __file__, 1, msg, None, None)

            Logger.consoleLogHandler.emit(record)
            Logger.consoleLogHandler.flush()
        except Exception as ex:
            print("!!!!log_msg got an exception: {}, msg={}, args={}, kw={}, traceback={}"
                  .format(ex, msg, args, kw, getTraceback(8)))

    def debug(self, msg=None, *args, **kw):
        msg = f"{msg}"
        if self.logLevel > logging.DEBUG:
            return
        self.log_msg(logging.DEBUG, msg, *args, **kw)

    def info(self, msg=None, *args, **kw):
        msg = f"{msg}"
        if self.logLevel > logging.INFO:
            return
        self.log_msg(logging.INFO, msg, *args, **kw)

    def warn(self, msg=None, *args, **kw):
        msg = f"{msg}"
        if self.logLevel > logging.WARNING:
            return
        self.log_msg(logging.WARNING, msg, *args, **kw)

    def error(self, msg=None, *args, **kw):
        msg = f"{msg}"
        if self.logLevel > logging.ERROR:
            return
        self.log_msg(logging.ERROR, msg, *args, **kw)
