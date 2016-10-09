from zope.interface import Interface
from uvc.api import api

class Mailtester(api.View):
    api.context(Interface)

    def render(self):
        return u"Hier wird die Mailadresse getestet"
