# -*- coding: utf-8 -*-
from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from pymongo import MongoClient
from bson.objectid import ObjectId
from App.config import getConfiguration
import xlwt
config = getConfiguration()
configuration = config.product_config.get('mongodb', dict())
mongoserver = configuration.get('mongoserver')
mongoport = int(configuration.get('mongoport'))



class Mailtester(api.Page):
    api.context(Interface)

    def render(self):
        recipient = self.context.email
        subject = u"Test-eMail für Stellenanzeige mit der Kennziffer: %s" %self.context.kennziffer
        body = u'Eingehende Bewerbungen für: "%s" werden an diese eMail-Adresse gesendet.' %self.context.title
        ploneapi.portal.send_email(
            recipient=recipient,
            sender="bghwportal@bghw.de",
            subject=subject,
            body=body,
            ) 
        return u"Bitte prüfen Sie Ihr Postfach, die Test-eMail wurde versendet."


class ReadData(api.View):
    api.context(Interface)

    def render(self):
        client = MongoClient(mongoserver, mongoport)
        kennziffer = self.request.get('kennziffer')
        pin = self.request.get('pin')
        database = 'db_%s' % (kennziffer)
        entries = client[database].collection.find()
