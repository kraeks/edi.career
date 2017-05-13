# -*- coding: utf-8 -*-
from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from pymongo import MongoClient
from bson.objectid import ObjectId
from App.config import getConfiguration
import xlwt
import tempfile
import hashlib
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

    def writeExcel(self, ws, row, i, pin):
        if pin == i.get('pin'):
            self.pincheck = True
        ws.write(row, 0, i.get('eingangsdatum'))
        ws.write(row, 1, str(i.get('_id')))
        if i.get('anrede') == 'Herr':
            geschlecht = 'm'
        else:
            geschlecht = 'w'
        ws.write(row, 2, '')
        ws.write(row, 3, geschlecht)
        ws.write(row, 4, i.get('titel'))
        ws.write(row, 5, i.get('vorname-1'))
        ws.write(row, 6, i.get('nachname-1'))
        ws.write(row, 7, i.get('strasse-hausnummer'))
        ws.write(row, 8, i.get('hausnummer'))
        ws.write(row, 9, i.get('adresszusatz'))
        ws.write(row, 10, i.get('postleitzahl'))
        ws.write(row, 11, i.get('ort'))
        ws.write(row, 12, i.get('telefonnummer-string'))
        ws.write(row, 13, i.get('replyto'))
        datum = i.get('geburtsdatum').split(' ')[0].split('-')
        geb = '%s.%s.%s' %(datum[2], datum[1], datum[0])
        ws.write(row, 14, geb)
        behindert = i.get('schwerbehinderung-gleichstellung-1')
        behindert = ','.join(behindert)
        ws.write(row, 15, behindert)
        ws.write(row, 16, i.get('hoechster-schulabschluss'))
        if i.get('schulabschluss-ist'):
            absolviert = i.get('schulabschluss-ist')[0]
            am = i.get('am')
            absolviertam = "%s am: %s" % (absolviert, am)
            ws.write(row, 17, absolviertam)
        ausbildung = studium = weiterbildung = ''
        if i.get('ausbildungsberuf'):
            ausbildung = '%s %s %s %s %s' %(i.get('ausbildungsberuf'),
                                            i.get('fachrichtung'),
                                            i.get('ausbildungsstaette'))
            ws.write(row, 18, ausbildung)
        if i.get('ausbildung-ist'):
            absolviert = i.get('ausbildung-ist')[0]
            am = i.get('am-1')
            absolviertam = "%s am: %s" %(absolviert, am)
            ws.write(row, 19, absolviertam)

        if i.get('studiengang'):
            studium = '%s %s %s %s %s' %(i.get('studiengang'),
                                         i.get('fachrichtung-1'),
                                         i.get('hochschule'))
            ws.write(row, 20, studium)
        if i.get('abschluss-ist'):
            absolviert = i.get('abschluss-ist')[0]
            am = i.get('am-2')
            absolviertam = "%s am: %s" %(absolviert, am)
            ws.write(row, 21, absolviertam)

        if i.get('ausbildungsberuf-studiengang'):
            weiterbildung = '%s %s %s %s %s' %(i.get('ausbildungsberuf-studiengang'),
                                               i.get('fachrichtung-2'),
                                               i.get('ausbildungsstaette-hochschule'))
            ws.write(row, 22, weiterbildung)
        if i.get('abschluss-ist-1'):
            absolviert = i.get('abschluss-ist-1')[0]
            am = i.get('am-3')
            absolviertam = "%s am: %s" %(absolviert, am)
            ws.write(row, 23, absolviertam)
        beruf = u"""\
Stellenbezeichnung: %s
Einsatzbereich/Abteilung: %s
Arbeitgeber: %s
von: %s
bis: %s
        """ %(i.get('stellenbezeichnung'),
              i.get('einsatzbereich-abteilung'),
              i.get('arbeitgeber'))
        ws.write(row, 24, beruf)
        berufdatum = "%s bis %s" % (i.get('von-seit'), i.get('bis'))
        ws.write(row, 25, berufdatum)

    def render(self):
        client = MongoClient(mongoserver, mongoport)
        kennziffer = self.request.get('kennziffer')
        pin = self.request.get('pin')
        print pin
        pin = hashlib.sha224(pin).hexdigest()
        print pin
        self.pincheck = False
        database = 'db_%s' % (kennziffer)
        entries = client[database].collection.find()
        wb = xlwt.Workbook()
        ws = wb.add_sheet('Bewerber')
        row = 0
        for i in entries:
             self.writeExcel(ws, row, i, pin)
             row += 1
        myfile = tempfile.TemporaryFile()
        if not self.pincheck:
            return self.response.redirect('novalidpin')
        wb.save(myfile)
        myfile.seek(0)
        filename = 'bewerber.xls'
        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', 'application/vnd.ms-excel')
        RESPONSE.setHeader('content-disposition', 'attachment; filename=%s' %filename)
        return myfile.read()


class NoValidPin(api.Page):
    api.context(Interface)


    def render(self):
        return u"Der von Ihnen eingegebene PIN ist nicht gültig"
