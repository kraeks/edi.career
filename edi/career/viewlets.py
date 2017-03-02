import hashlib
from DateTime import DateTime
from uvc.api import api
from zope.interface import Interface
from Products.ATContentTypes.interfaces import IATNewsItem
from plone.app.layout.viewlets.interfaces import IBelowContentBody
from plone import api as ploneapi

api.templatedir('templates')

class CareerFormViewlet(api.Viewlet):
    api.context(IATNewsItem)
    api.viewletmanager(IBelowContentBody)

    def available(self):
        if self.context.getReferences('rel_careerform'):
            return True
        return False

    def update(self):
        if self.available():
            ref = self.context.getReferences('rel_careerform')[0]
            kennziffer = getattr(self.context, 'kennziffer', '')
            pin = getattr(self.context, 'pin', '')
            mail = getattr(self.context, 'email', '')
            pin = hashlib.sha224(pin).hexdigest()
            self.linkurl = "%s?kennziffer=%s&pin=%s&stellentitel=%s/%s&mykennziffer=%s&empfaenger=%s" % (ref.absolute_url(), 
                                                                                        kennziffer, 
                                                                                        pin,
                                                                                        self.context.title,
                                                                                        kennziffer,
                                                                                        kennziffer,
                                                                                        mail)
            bewerbungsfrist = getattr(self.context, 'bewerbungsfrist')
            if bewerbungsfrist:
                self.bewerbungsfrist = bewerbungsfrist.strftime('%d.%m.%Y')
            else:
                self.bewerbungsfrist = ''
            self.ansprechperson = getattr(self.context, 'ansprechperson')
            self.telefon = getattr(self.context, 'telefon')

class TestEMailViewlet(api.Viewlet):
    api.context(IATNewsItem)
    api.viewletmanager(IBelowContentBody)

    def available(self):
        try:
            current = ploneapi.user.get_current()
            return ploneapi.user.has_permission('Modify portal content', username=current.id, obj=self.context)
        except:
            return False

    def update(self):
        self.testmailurl = self.context.absolute_url() + '/mailtester'
