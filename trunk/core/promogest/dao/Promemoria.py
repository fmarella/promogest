# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
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

import datetime
from sqlalchemy import Table
from sqlalchemy.orm import mapper
from promogest.Environment import params
from Dao import Dao

class Promemoria(Dao):
    """ User class provides to make a Users dao which include more used"""

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

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


def updateScadenzePromemoria():
    """ Segna quali promemoria entrano nel periodo in scadenza,
        quali scadono, e quali sono completati """
    promes = Promemoria().select(in_scadenza=False, completato=False)
    for p in promes:
        preavviso = p.giorni_preavviso
        data_attuale = datetime.datetime.now()
        data_scadenza = p.data_scadenza
        if data_scadenza < data_attuale:
            p.scaduto = True
            Environment.session.add(p)
        elif data_scadenza > data_attuale:
            differenze = int((data_scadenza - data_attuale).days)
            if differenze < preavviso:
                p.in_scadenza = True
                Environment.session.add(p)
        Environment.session.commit()


def getScadenze():
    """
    Ritorna una lista di id di oggetti Promemoria in scadenza (e quindi da notificare)
    """
    alarms = Promemoria().select(in_scadenza=True,offset=None, batchSize=None)
    #returnList = []
    #if alarms:
        #for alarm in alarms:
            #returnList.append(alarm.id)
    #return returnList
    return alarms

#if params['schema'] + ".promemoria" in metatmp.tables.keys():
    #t = metatmp.tables[params['schema'] + ".promemoria"]
    #t.tometadata(meta)
    #promemoria = Table('promemoria',
                #params['metadata'],
                #schema = params['schema'],
                #autoload=True)

promemoria = Table('promemoria',
            params['metadata'],
            schema = params['schema'],
            autoload=True)

std_mapper= mapper(Promemoria, promemoria, order_by=promemoria.c.id)
