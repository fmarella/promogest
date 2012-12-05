# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    Promogest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Promogest.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import params
import datetime
from sqlalchemy.ext.serializer import loads, dumps
from promogest.lib.utils import messageError


class ApplicationLog(object):

    def __init__(self, req=None):
        pass

    def store(self, dao=None,action=None,status=True,value=None ):
        self.dao = dao
        self.action = action
        self.status = status
        self.value = value
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
            messageError(msg=msg, transient=None)
            print "ERRORE", e
            params["session"].rollback()
            return False



    def saveToAppLog(self):
            if self.action:
                if self.value:
                    esito = " ERRATO"
                    how = "E"
                else:
                    esito = " CORRETTO"
                    how = "I"
                message = self.action + esito
            else:
                if params["session"].dirty:
                    message = "UPDATE "+ self.dao.__class__.__name__
                elif params["session"].new:
                    message = "INSERT " + self.dao.__class__.__name__
                elif params["session"].deleted:
                    message = "DELETE "+ self.dao.__class__.__name__
                else:
                    message = "UNKNOWN ACTION"

            when = datetime.datetime.now()
            where = params['schema']
            whoID = params['usernameLoggedList'][0]
            utentedb = params['usernameLoggedList'][3]
            utente = params['usernameLoggedList'][1]

            if self.action:
                whatstr= self.value
            else:
                salvo = self.commit()
                if salvo:
                    how = "I"
                else:
                    how = "E"
                mapper = object_mapper(self.dao)
                pk = mapper.primary_key_from_instance(self.dao)
                whatstr = str(pk)

            app = ApplicationLog()
            app.schema = where
            app.message = message
            app.level = how
            print dumps(whatstr)
            app.strvalue = dumps(whatstr)
            app.registrazion_date = when
            app.utentedb = utentedb
            app.id_utente = whoID
            app.pkid = dumps(whatstr)
            print dumps(self.dao)
            app.object = dumps(self.dao)
            params["session"].add(app)
            self.commit()
            print "[LOG] %s id: %s da %s in %s in data %s" %(message, whatstr,utente, where ,when.strftime("%d/%m/%Y"))


appLogTable = Table('application_log', params['metadata'], autoload=True, schema=params['mainSchema'])
std_mapper = mapper(ApplicationLog, appLogTable, order_by=appLogTable.c.id_utente)
