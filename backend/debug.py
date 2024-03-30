import os
import sys
import codecs
import datetime
import traceback

from collections.abc import Iterable

IsDebug                = 1  # sa[stdout]: prints general info (1 - forbidden with apache!)
IsDeepDebug            = 0  # sa[stdout]: prints detailed info (1 - forbidden with apache!)
IsTrace                = 0  # Trace[errorlog]: output execution trace for http-requests
IsPrintExceptions      = 1  # Flag: sets printing of exceptions
IsDisableOutput        = 0  # Flag: disabled stdout

basedir = os.path.abspath(os.path.dirname(__file__))
errorlog = os.path.join(basedir, 'traceback.log')

LOCAL_FULL_TIMESTAMP   = '%d-%m-%Y %H:%M:%S'
LOCAL_EXCEL_TIMESTAMP  = '%d.%m.%Y %H:%M:%S'
LOCAL_EASY_TIMESTAMP   = '%d-%m-%Y %H:%M'
LOCAL_EASY_DATESTAMP   = '%Y-%m-%d'
LOCAL_EXPORT_TIMESTAMP = '%Y%m%d%H%M%S'
UTC_FULL_TIMESTAMP     = '%Y-%m-%d %H:%M:%S'
UTC_EASY_TIMESTAMP     = '%Y-%m-%d %H:%M'
DATE_TIMESTAMP         = '%d/%m'
DATE_STAMP             = '%Y%m%d'

default_unicode        = 'utf-8'
default_encoding       = default_unicode

# ---------------------------- #

ansi = None

n_a = 'n/a'
cr = '\n'

def isIterable(v):
    return not isinstance(v, str) and isinstance(v, Iterable)


#######################################################################


def print_to(f, v, mode='ab', request=None, encoding=default_encoding):
    if IsDisableOutput:
        return
    items = not isIterable(v) and [v] or v
    if not f:
        f = getErrorlog()
    fo = open(f, mode=mode)
    def _out(s):
        if not isinstance(s, bytes):
            fo.write(s.encode(encoding, 'ignore'))
        else:
            fo.write(s)
        fo.write(cr.encode())
    for text in items:
        try:
            if IsDeepDebug or IsTrace:
                print(text)
            if request is not None:
                _out('%s>>> %s [%s]' % (cr, datetime.datetime.now().strftime(UTC_FULL_TIMESTAMP), request.url))
            _out(text)
        except Exception as e:
            pass
    fo.close()

def print_exception(stack=None, request=None):
    print_to(errorlog, 
        '%s>>> %s:%s' % (cr, datetime.datetime.now().strftime(LOCAL_FULL_TIMESTAMP), cr), 
        request=request)
    traceback.print_exc(file=open(errorlog, 'a'))
    if stack is not None:
        print_to(errorlog, '%s>>> Traceback stack:%s' % (cr, cr))
        traceback.print_stack(file=open(errorlog, 'a'))

def getErrorlog():
    return errorlog

def getCurrentDate():
    return datetime.datetime.now().strftime(LOCAL_EASY_DATESTAMP)
