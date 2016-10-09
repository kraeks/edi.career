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
        del mydict['anschreiben_file']
        del mydict['form.submitted']
        del mydict['add_reference']
        mydict['pin'] = pin
        myid = client[database].collection.insert_one(mydict)
        ##Test##
        anrede = self.request.form.get('anrede')
        titel = self.request.form.get('titel')
        vorname = self.request.form.get('vorname-1')
        nachname = self.request.form.get('nachname-1')
        online = str(myid.inserted_id)

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Bewerber')

        ws.write(0, 0, anrede)
        ws.write(0, 1, online)
        ws.write(0, 2, titel)
        ws.write(0, 3, '')
        ws.write(0, 4, vorname)
        ws.write(0, 5, nachname)
        wb.save('/Users/larswalther/Desktop/example.xls')
        return 'test'
