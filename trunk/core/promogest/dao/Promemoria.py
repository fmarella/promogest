# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: FRancesco Meloni <francesco@promotux.it>

from promogest.lib.sqlalchemy import *
from promogest.lib.sqlalchemy.orm import *
from promogest.Environment import *
from promogest import Environment
from Dao import Dao
import datetime

class Promemoria(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, arg=None,isList=False, id=None):
        Dao.__init__(self, entity=self.__class__, isList=isList, id=id)

    def filter_values(self,k,v):
        if k=="incaricato":
            dic = { k : promemoria.c.incaricato.ilike("%"+v+"%") }
        elif k == 'in_scadenza':
            dic = { k :promemoria.c.in_scadenza ==v}
        elif k == 'scaduto':
            dic = { k :promemoria.c.scaduto ==v}
        elif k == "autore":
            dic = { k : promemoria.c.autore.contains(v)}
        elif k == "annotazione":
            dic = { k : promemoria.c.annotazione.ilike("%"+v+"%") }
        elif k == "riferimento":
            dic = { k: promemoria.c.riferimento.ilike("%"+v+"%")}
        elif k == "completato":
            dic = { k:promemoria.c.completato == v }
        elif k == "descrizione":
            dic = { k:promemoria.c.descrizione.ilike("%"+v+"%") }
        elif k == "oggetto":
            dic = { k:promemoria.c.oggetto.ilike("%"+v+"%") }
        elif k == "a_data_scadenza":
            dic = { k:promemoria.c.data_scadenza <= v }
        elif k == "da_data_scadenza":
            dic = { k:promemoria.c.data_scadenza >= v }
        elif k == "a_data_inserimento":
            dic = { k:promemoria.c.data_inserimento <= v }
        elif k == "da_data_inserimento":
            dic = { k:promemoria.c.data_inserimento >= v }
        return  dic[k]

def getScadenze():
    """
    Ritorna una lista di id di oggetti Promemoria in scadenza (e quindi da notificare)
    """
    alarms = Promemoria(isList=True).select(in_scadenza=True,offset=None, batchSize=None)
    returnList = []
    for alarm in alarms:
        returnList.append(alarm.id)
    return returnList

def updateScadenze():
    #FIXME " ATTENZIONE :parte commentata e da rifare su pg2
    """ Segna quali promemoria entrano nel periodo in scadenza, quali scadono, e quali sono completati """
    #Environment.connection.execStoredProcedure('ScadenzePromemoriaUpd',())
    pass

promemoria = Table('promemoria',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper= mapper(Promemoria, promemoria, order_by=promemoria.c.id)