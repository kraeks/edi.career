# -*- coding: utf-8 -*-
from zope.interface import Interface
from edi.career.interfaces import IBewerbungen
from uvc.api import api
from plone import api as ploneapi
import urllib

class DownloadBewerbungen(api.Form):
    api.context(Interface)
    fields = api.Fields(IBewerbungen)


    @api.action('Download')
    def handle_download(self):
        data, errors = self.extractData()
        if errors:
            return
        data['handling'] = 'download'
        baseurl = ploneapi.portal.get().absolute_url()
        params = urllib.urlencode(data)
        url = '%s/readdata?%s' % (baseurl, params)
        return self.response.redirect(url)


class EmailBewerbungen(api.Form):
    api.context(Interface)
    fields = api.Fields(IBewerbungen)


    @api.action('Senden')
    def handle_download(self):
        data, errors = self.extractData()
        if errors:
            return
        data['handling'] = 'mail'
        baseurl = ploneapi.portal.get().absolute_url()
        params = urllib.urlencode(data)
        url = '%s/readdata?%s' % (baseurl, params)
        return self.response.redirect(url)

