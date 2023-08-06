===============
pywe-marketcode
===============

Wechat MarketCode Module for Python.

Installation
============

::

    pip install pywe-marketcode


Usage
=====

::

    from pywe_marketcode import MarketCode, applycode, applycodequery, applycodedownload, codeactive, codeactivequery, tickettocode


Method
======

::

    class MarketCode(BaseToken):
        def __init__(self, appid=None, secret=None, token=None, storage=None):
            super(MarketCode, self).__init__(appid=appid, secret=secret, token=token, storage=storage)

        def applycode(self, isv_application_id, code_count, appid=None, secret=None, token=None, storage=None):

        def applycodequery(self, isv_application_id, application_id, appid=None, secret=None, token=None, storage=None):

        def applycodedownload(self, application_id, code_start, code_end, appid=None, secret=None, token=None, storage=None, decrypted=True):

        def codeactive(self, application_id, activity_name, product_brand, product_title, product_code, wxa_appid, wxa_path, code_start, code_end, wxa_type=0, appid=None, secret=None, token=None, storage=None):

        def codeactivequery(self, application_id=None, code_index=None, code=None, code_url=None, appid=None, secret=None, token=None, storage=None):

        def tickettocode(self, code_ticket, openid, appid=None, secret=None, token=None, storage=None):

