from datetime import datetime
from zope.interface import Interface
from uvc.api import api 
from pymongo import MongoClient
from bson.objectid import ObjectId
from App.config import getConfiguration
import xlwt
config = getConfiguration()
configuration = config.product_config.get('mongodb', dict())
mongoserver = configuration.get('mongoserver')
mongoport = int(configuration.get('mongoport'))


class careerworker(api.View):
    api.context(Interface)

    def render(self):
        client = MongoClient(mongoserver, mongoport)
        kennziffer = self.request.form.get('kennziffer')
        pin = self.request.form.get('pin')
        database = 'db_%s' % (kennziffer)
        mydict = self.request.form
        dbentry = {}
        for i in mydict.keys():
            if i not in ['anschreiben_file', 'form.submitted', 'add_reference']:
                dbentry[i] = mydict[i]
        dbentry['pin'] = pin
        dbentry['eingangsdatum'] = datetime.now().strftime('%d.%m.%Y')
        myid = client[database].collection.insert(dbentry)
