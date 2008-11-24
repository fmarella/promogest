# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from promogest.dao.Dao import Dao

#params['schema']
#params['metadata']
#def create()
#if hasattr(conf, 'PromoWear'):
#if conf.PromoWear.primoavvio=="yes":
""" tabelle schema principale """

listinoArticoloTable = Table('listino_articolo', params['metadata'], autoload=True, schema=params['schema'])
scontoTable = Table('sconto', params['metadata'], autoload=True, schema=params['schema'])

scontiVenditaIngrossoTable = Table('sconti_vendita_ingrosso', params['metadata'],
        Column('id',Integer,ForeignKey(params['schema']+'.sconto.id',onupdate="CASCADE",ondelete="CASCADE"), primary_key=True),
        Column('id_listino',Integer),
        Column('id_articolo',Integer),
        Column('data_listino_articolo',DateTime),
        ForeignKeyConstraint(columns=("id_listino","id_articolo","data_listino_articolo"),
                                        refcolumns=(params['schema']+'.listino_articolo.id_listino',
                                                    params['schema']+'.listino_articolo.id_articolo',
                                                    params['schema']+'.listino_articolo.data_listino_articolo'),
                                        onupdate="CASCADE", ondelete="CASCADE"),

        schema=params['schema']
        )

scontiVenditaIngrossoTable.create(checkfirst=True)
print "CREATO sconti_vendita_ingrosso"

scontiVenditaDettaglioTable = Table('sconti_vendita_dettaglio',params['metadata'],
        Column('id',Integer,ForeignKey(params['schema']+'.sconto.id',onupdate="CASCADE",ondelete="CASCADE"), primary_key=True),
        Column('id_listino',Integer),
        Column('id_articolo',Integer),
        Column('data_listino_articolo',DateTime),
        ForeignKeyConstraint(columns=("id_listino","id_articolo","data_listino_articolo"),
                                        refcolumns=(params['schema']+'.listino_articolo.id_listino',
                                                    params['schema']+'.listino_articolo.id_articolo',
                                                    params['schema']+'.listino_articolo.data_listino_articolo'),
                                        onupdate="CASCADE", ondelete="CASCADE"),
        schema=params['schema']
        )
scontiVenditaDettaglioTable.create(checkfirst=True)
print "CREATO sconti_vendita_dettaglio"

