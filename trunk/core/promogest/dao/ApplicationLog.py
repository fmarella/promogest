# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import gtk
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import params
import datetime

class ApplicationLog(object):

    def __init__(self, arg=None):
        pass


    def persist(self, dao=None):
        self.dao = dao
        #print self.dao, dir(self.dao), self.dao.__repr__, self.dao.__class__.__name__,self.dao.__module__
        self.saveToAppLog()


    def commit(self):
        """ Salva i dati nel DB"""
        try:
            params["session"].commit()
            return True
        except Exception,e:
            msg = """ATTENZIONE ERRORE
Qui sotto viene riportato l'errore di sistema:
%s
( normalmente il campo in errore è tra "virgolette")
""" %e
            overDialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL
                                                | gtk.DIALOG_DESTROY_WITH_PARENT,
                                                    gtk.MESSAGE_ERROR,
                                                    gtk.BUTTONS_CANCEL, msg)
            response = overDialog.run()
            overDialog.destroy()
            print "ERRORE", e
            params["session"].rollback()
            return False



    def saveToAppLog(self):
            when = datetime.datetime.now()
            where = params['schema']
            whoID = params['usernameLoggedList'][0]
            utentedb = params['usernameLoggedList'][3]
            utente = params['usernameLoggedList'][1]

            if params["session"].dirty:
                message = "UPDATE "+ self.dao.__class__.__name__
            elif params["session"].new:
                message = "INSERT " + self.dao.__class__.__name__
            elif params["session"].deleted:
                message = "DELETE "+ self.dao.__class__.__name__
            else:
                message = "UNKNOWN ACTION"
            mapper = object_mapper(self.dao)
            salvo = self.commit()
            if salvo:
                how = "I"
            else:
                how = "E"

            pk = mapper.primary_key_from_instance(self.dao)

            whatstr = str(pk)
            app = ApplicationLog()
            app.schema = where
            app.message = message
            app.level = how
            app.strvalue = whatstr
            app.registrazion_date = when
            app.utentedb = utentedb
            app.id_utente = whoID
            app.pkid = whatstr
            app.object = str(self.dao.__class__)
            params["session"].add(app)
            self.commit()
            print "[LOG] %s id: %s da %s in %s in data %s" %(message, whatstr,utente, where ,when.strftime("%d/%m/%Y"))


appLogTable = Table('application_log', params['metadata'], autoload=True, schema=params['mainSchema'])
std_mapper = mapper(ApplicationLog, appLogTable, order_by=appLogTable.c.id_utente)
