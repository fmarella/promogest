# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

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
    def __init__(self, arg=None):
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