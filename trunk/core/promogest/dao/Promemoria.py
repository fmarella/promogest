# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao, Base

class Promemoria(Base, Dao):
    """ User class provides to make a Users dao which include more used"""
    try:
        __table__ = Table('promemoria',
            params['metadata'],
            schema = params['schema'],
            autoload=True)
    except:
        from data.promemoria import t_promemoria
        __table__ = t_promemoria

    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k=="incaricato":
            dic = { k : Promemoria.__table__.c.incaricato.ilike("%"+v+"%") }
        elif k == 'in_scadenza':
            dic = { k :Promemoria.__table__.c.in_scadenza ==v}
        elif k == 'scaduto':
            dic = { k :Promemoria.__table__.c.scaduto ==v}
        elif k == "autore":
            dic = { k : Promemoria.__table__.c.autore.contains(v)}
        elif k == "annotazione":
            dic = { k : Promemoria.__table__.c.annotazione.ilike("%"+v+"%") }
        elif k == "riferimento":
            dic = { k: Promemoria.__table__.c.riferimento.ilike("%"+v+"%")}
        elif k == "completato":
            dic = { k:Promemoria.__table__.c.completato == v }
        elif k == "descrizione":
            dic = { k:Promemoria.__table__.c.descrizione.ilike("%"+v+"%") }
        elif k == "oggetto":
            dic = { k:Promemoria.__table__.c.oggetto.ilike("%"+v+"%") }
        elif k == "a_data_scadenza":
            dic = { k:Promemoria.__table__.c.data_scadenza <= v }
        elif k == "da_data_scadenza":
            dic = { k:Promemoria.__table__.c.data_scadenza >= v }
        elif k == "a_data_inserimento":
            dic = { k:Promemoria.__table__.c.data_inserimento <= v }
        elif k == "da_data_inserimento":
            dic = { k:Promemoria.__table__.c.data_inserimento >= v }
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
            session.add(p)
        elif data_scadenza > data_attuale:
            differenze = int((data_scadenza - data_attuale).days)
            if differenze < preavviso:
                p.in_scadenza = True
                session.add(p)
        session.commit()


def getScadenze():
    """
    Ritorna una lista di id di oggetti Promemoria in scadenza (e quindi da notificare)
    """
    alarms = Promemoria().select(in_scadenza=True,offset=None, batchSize=None)
    return alarms
