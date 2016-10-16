# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.schema import TextLine
from uvc.api import api

class IBewerbungen(Interface):

    kennziffer = TextLine(title = u'Kennziffer',
                          description = u'Bitte geben Sie hier die Kennziffer der Stellenanzeige ein.')

    pin = TextLine(title = u'PIN',
                   description = u'Bitte geben Sie hier den Sicherheits-PIN für die Stellenanzeige ein.')

