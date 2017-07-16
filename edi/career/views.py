# -*- coding: utf-8 -*-
from zope.interface import Interface
from uvc.api import api
from plone import api as ploneapi
from pymongo import MongoClient
from bson.objectid import ObjectId
from App.config import getConfiguration
from Products.CMFPlone.utils import getToolByName
import xlwt
import tempfile
import hashlib
config = getConfiguration()
configuration = config.product_config.get('mongodb', dict())
mongoserver = configuration.get('mongoserver')
mongoport = int(configuration.get('mongoport'))
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

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
        if i.get('anrede') == 'geehrter Herr':
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
        schulabschluss = i.get('hoechster-schulabschluss')
        absolviertam = ''
        if i.get('schulabschluss-ist'):
            absolviert = i.get('schulabschluss-ist')
            am = i.get('am')
            am = '%s.%s.%s' %(am[8:10],am[5:7],am[0:4])
            absolviertam = "%s am: %s" % (absolviert, am)
        schulabschluss = "%s %s" %(schulabschluss, absolviertam)
        ws.write(row, 16, schulabschluss)

        ausbildung = ''
        absolviertam = ''
        if i.get('ausbildungsberuf'):
            ausbildung = '%s %s %s' %(i.get('ausbildungsberuf'),
                                      i.get('fachrichtung'),
                                      i.get('ausbildungsstaette'))
        if i.get('ausbildung-ist'):
            absolviert = i.get('ausbildung-ist')
            am = i.get('am-1')
            am = '%s.%s.%s' %(am[8:10],am[5:7],am[0:4])
            absolviertam = "%s am: %s" %(absolviert, am)
        ausbildung = "%s %s" %(ausbildung, absolviertam)
        ws.write(row, 17, ausbildung)

        studium = ''
        absolviertam =''
        if i.get('studiengang'):
            studium = '%s %s %s' %(i.get('studiengang'),
                                   i.get('fachrichtung-1'),
                                   i.get('hochschule'))
        if i.get('abschluss-ist'):
            absolviert = i.get('abschluss-ist')
            am = i.get('am-2')
            am = '%s.%s.%s' %(am[8:10],am[5:7],am[0:4])
            absolviertam = "%s am: %s" %(absolviert, am)
        studium = "%s %s" %(studium, absolviertam)
        ws.write(row, 18, studium)

        weiterbildung = ''
        absolviertam = ''
        if i.get('ausbildungsberuf-studiengang'):
            weiterbildung = '%s %s %s' %(i.get('ausbildungsberuf-studiengang'),
                                         i.get('fachrichtung-2'),
                                         i.get('ausbildungsstaette-hochschule'))
        if i.get('abschluss-ist-1'):
            absolviert = i.get('abschluss-ist-1')
            am = i.get('am-3')
            am = '%s.%s.%s' %(am[8:10],am[5:7],am[0:4])
            absolviertam = "%s am: %s" %(absolviert, am)
        weiterbildung = "%s %s" %(weiterbildung, absolviertam)
        ws.write(row, 19, weiterbildung)

        beruf = ''
        beruf = '%s %s %s' %(i.get('stellenbezeichnung'),
                             i.get('einsatzbereich-abteilung'),
                             i.get('arbeitgeber'))
        vonseit = i.get('von-seit')
        if vonseit:
            vonseit = '%s.%s.%s' %(vonseit[8:10],vonseit[5:7],vonseit[0:4])
        else:
            vonseit = ''
        bis = i.get('bis')
        if bis:
            bis = '%s.%s.%s' %(bis[8:10],bis[5:7],bis[0:4])
        else:
            bis = ''
        berufdatum = "%s bis %s" % (vonseit, bis)
        beruf = "%s %s" %(beruf, berufdatum)
        ws.write(row, 20, beruf)

    def send_mail(self, send_from, send_to, subject, text, files=[], server="127.0.0.1", kennziffer="bewerbungen"):
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        for f in files:
            part = MIMEApplication(f.read(), Name='%s.xls' %str(kennziffer))
            part['Content-Disposition'] = 'attachment; filename="%s.xls"' %str(kennziffer)
            msg.attach(part)

        smtp = smtplib.SMTP(server)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()

    def render(self):
        client = MongoClient(mongoserver, mongoport)
        kennziffer = self.request.get('kennziffer')
        pin = self.request.get('pin')
        handling = self.request.get('handling')
        pin = hashlib.sha224(pin).hexdigest()
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
        if handling == 'download':
            filename = 'bewerber.xls'
            RESPONSE = self.request.response
            RESPONSE.setHeader('content-type', 'application/vnd.ms-excel')
            RESPONSE.setHeader('content-disposition', 'attachment; filename=%s' %filename)
            return myfile.read()
        elif handling == 'mail':
            pcat = getToolByName(self.context, 'portal_catalog')
            brains = pcat(Kennziffer=kennziffer, show_inactive=True)
            if brains:
                send_to = brains[0].getObject().email
            else:
                return self.response.redirect('novalidpin')
            send_from = 'bghwportal@bghw.de'
            subject = u'Bewerbungen auf Stellenanzeige mit Kennziffer: %s' % kennziffer
            text = u'Hier erhalten Sie die Excel-Datei mit den eingegangenen Bewerbungen'
            files = [myfile]
            server = self.context.MailHost.get('smtp_host')
            server = "10.30.0.57"
            self.send_mail(send_from, send_to, subject, text, files, server, kennziffer)
            return self.response.redirect('mailsent')

class NoValidPin(api.Page):
    api.context(Interface)


    def render(self):
        return u"Es wurde keine Stellenanzeige mit dieser Kennziffer gefunden oder der von Ihnen eingegebene PIN ist nicht gültig"

class MailSent(api.Page):
    api.context(Interface)

    def render(self):
        return u"Es wurde eine eMail an das in der Stellenanzeige angegebene Postfach gesendet."
