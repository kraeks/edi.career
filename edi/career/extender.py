# -*- coding: utf-8 -*-
# Copyright (c) 2016 educorvi GmbH & Co. KG
# walther.educorvi@gmail.com
from zope.component import adapts
from zope.interface import implements
from DateTime import DateTime
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.public import StringWidget, SelectionWidget, ImageWidget, BooleanWidget, ReferenceWidget, PasswordWidget
from Products.Archetypes.public import CalendarWidget
from Products.Archetypes.atapi import StringField, ReferenceField, ImageField, BooleanField, LinesField
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import DisplayList
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.ATContentTypes.content.newsitem import ATNewsItem
from Products.Archetypes.atapi import AnnotationStorage
from Products.ATContentTypes.configuration import zconf

from Products.validation import V_REQUIRED

from archetypes.schemaextender.field import ExtensionField

class CustomReferenceField(ExtensionField, ReferenceField):
    pass

class CustomStringField(ExtensionField, StringField):
    pass

class CustomDateTimeField(ExtensionField, DateTimeField):
    pass

extension_fields = [
               CustomReferenceField('careerform',
               schemata=u'Karriere',
               relationship='rel_careerform',
               multiValued=False,
               widget = ReferenceBrowserWidget(
                           label = u"Online-Bewerbung",
                           description = u"Soll die Stelle ein Online-Bewerbungsformular erhalten? Bitte hier eintragen.",
                           startup_directory = '/',
                           destination_types = ('FormFolder',),
                           force_close_on_insert = True,
                           ),
                 ),
               CustomStringField('kennziffer',
               schemata=u'Karriere',
               widget = StringWidget(
                           label = u"Kennziffer",
                           description = u"Bitte tragen Sie hier die Kennziffer der Bewerbung ein.",
                           ),
                 ),
               CustomStringField('pin',
               schemata=u'Karriere',
               widget = StringWidget(
                           label = u"PIN",
                           description = u"Bitte geben Sie hier einen 4-stelligen PIN-Code zum Schutz der Bewerberdaten ein.",
                           size = 4,
                           maxlength = 4,
                           ),
               ),
               CustomStringField('email',
               schemata=u'Karriere',
               validators = ('isEmail'),
               default = "karriere@bghw.de",
               widget = StringWidget(
                           label = u"eMail",
                           description = u"Bitte geben Sie hier ein, an welche eMail-Adresse die\
                                           Bewerbungsdaten geschickt werden sollen,",
                           ),
                 ),
               CustomStringField('ansprechperson',
               schemata=u'Karriere',
               widget = StringWidget(
                           label = u"Ansprechperson",
                           ),
                 ),
               CustomStringField('telefon',
               schemata=u'Karriere',
               default=u"+49 (0) 621 183-5251",
               widget = StringWidget(
                           label = u"Telefonnummer der Ansprechperson",
                           ),
                 ),
               CustomDateTimeField('bewerbungsfrist',
               schemata=u'Karriere',
               widget = CalendarWidget(
                           label = u"Bewerbungsfrist",
                           format = '%d.%m.%Y',
                           show_hm = False,
                           default_method = 'getDefaultTime',
                           ),
               ),
               ]

def getDefaultTime(self):
    return DateTime()

class CareerNewsItemExtender(object):
    adapts(ATNewsItem)
    implements(ISchemaExtender)
    fields = extension_fields

    def __init__(self, context):
         self.context = context

    def getFields(self):
         return self.fields

