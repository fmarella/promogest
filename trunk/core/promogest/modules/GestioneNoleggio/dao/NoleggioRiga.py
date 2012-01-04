# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni <francesco@promotux.it>

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
from promogest.Environment import *
from promogest.dao.Dao import Dao

class NoleggioRiga(Dao):
    """ TABELLA:  riga_dati_noleggio,
        questo dao gestisce la tabella di integrazioen dati su riga:
        per il noleggio è necessario infatti salvare diverse informazioni :
        coeficente di noleggio: ( salvato in articolo può essere modificato in sede
                                di creazione documento)
        numero giorni : ( risultato dalla differenza tra le due date di noleggio
                        é il caso di salvarlo per poter incrociare i dati e perchè
                        sento che a breve sarà necessario gestire archi temporali per riga)
    """
    def __init__(self, req=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'id':
            dic= {k:riganoleggio.c.id ==v}
        return  dic[k]


try:
    riganoleggio = Table('riga_dati_noleggio', params['metadata'],
                                    schema = params['schema'], autoload=True)
except:
    rigaTable = Table('riga', params['metadata'], autoload=True, schema=params['schema'])

    if tipodb == "sqlite":
        rigaFK = 'riga.id'
    else:
        rigaFK = params['schema']+'.riga.id'

    riganoleggio = Table('riga_dati_noleggio', params['metadata'],
                        Column('id',Integer,primary_key=True),
                        Column('isrent', Boolean,nullable=False),
                        Column('prezzo_acquisto',Numeric(16,4),nullable=True),
                        Column('coeficente',Numeric(16,4),nullable=True),
                        Column('id_riga',Integer,ForeignKey(rigaFK, onupdate="CASCADE", ondelete="RESTRICT"),nullable=False),
                        UniqueConstraint('id_riga'),
                        schema=params['schema'])
    riganoleggio.create(checkfirst=True)


std_mapper = mapper(NoleggioRiga, riganoleggio,properties={
                    }, order_by=riganoleggio.c.id)
