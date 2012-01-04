# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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


from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
import datetime



#params['schema']
#params['metadata']
#def create()
#if hasattr(conf, 'PromoWear'):
#if conf.PromoWear.primoavvio=="yes":
""" tabelle schema principale """

ccardTypeTable = Table('credit_card_type', params['metadata'],
        Column('id', Integer, primary_key=True),
        Column('denominazione', String(200), nullable=False ),
        Column('denominazione_breve', String(10), nullable=False),
        schema=params['schema'],
        )
ccardTypeTable.create(checkfirst=True)



#listinoArticoloTable = Table('listino_articolo', params['metadata'], autoload=True, schema=params['schema'])
#scontoTable = Table('sconto', params['metadata'], autoload=True, schema=params['schema'])

#scontiVenditaIngrossoTable = Table('sconti_vendita_ingrosso', params['metadata'],
        #Column('id',Integer,ForeignKey(params['schema']+'.sconto.id',onupdate="CASCADE",ondelete="CASCADE"), primary_key=True),
        #Column('id_listino',Integer),
        #Column('id_articolo',Integer),
        #Column('data_listino_articolo',DateTime),
        #ForeignKeyConstraint(columns=("id_listino","id_articolo","data_listino_articolo"),
                                        #refcolumns=(params['schema']+'.listino_articolo.id_listino',
                                                    #params['schema']+'.listino_articolo.id_articolo',
                                                    #params['schema']+'.listino_articolo.data_listino_articolo'),
                                        #onupdate="CASCADE", ondelete="CASCADE"),

        #schema=params['schema']
        #)
#try:
#app_table = Table('app_log', params['metadata'],
        #Column('id', Integer, primary_key=True),
        #Column('id_utente', Integer),
        #Column('utentedb', String(100), nullable=False),
        #Column('schema_azienda', String(100), nullable=False),
        #Column('level', String(1)),
        #Column('object', PickleType, nullable=True),
        #Column('message', String(1000), nullable=True),
        #Column('value', Integer, nullable=True),
        #Column('registration_date', DateTime),
        #schema=params['mainSchema'])

#app_table.create(checkfirst=True)

#primy_keyTable = Table('chiavi_primarie_log', params['metadata'],
        #Column('id', Integer, primary_key=True),
        #Column('pk_integer', Integer, nullable=True),
        #Column('pk_string', String(300), nullable=True),
        #Column('pk_datetime', DateTime,nullable=True),
        #Column('id_application_log2', Integer,ForeignKey(params['mainSchema']+'.app_log.id',onupdate="CASCADE",ondelete="CASCADE"), nullable=False),
        #schema=params['mainSchema'])
#primy_keyTable.create(checkfirst=True)
#except:
    #print "pppp"

#scontiVenditaIngrossoTable.create(checkfirst=True)
#print "CREATO sconti_vendita_ingrosso"

#scontiVenditaDettaglioTable = Table('sconti_vendita_dettaglio',params['metadata'],
        #Column('id',Integer,ForeignKey(params['schema']+'.sconto.id',onupdate="CASCADE",ondelete="CASCADE"), primary_key=True),
        #Column('id_listino',Integer),
        #Column('id_articolo',Integer),
        #Column('data_listino_articolo',DateTime),
        #ForeignKeyConstraint(columns=("id_listino","id_articolo","data_listino_articolo"),
                                        #refcolumns=(params['schema']+'.listino_articolo.id_listino',
                                                    #params['schema']+'.listino_articolo.id_articolo',
                                                    #params['schema']+'.listino_articolo.data_listino_articolo'),
                                        #onupdate="CASCADE", ondelete="CASCADE"),
        #schema=params['schema']
        #)
#scontiVenditaDettaglioTable.create(checkfirst=True)
#print "CREATO sconti_vendita_dettaglio"

# aggiunta delle due tabelle listino_complesso_listino e listino_complesso_articolo_prevalente
#listinoComplessoListinoTable = Table('listino_complesso_listino',params['metadata'],
        #Column('id_listino_complesso',Integer, primary_key=True),
        #Column('id_listino', Integer,ForeignKey(params['schema']+'.listino.id',onupdate="CASCADE",ondelete="CASCADE"),primary_key=True),
        #schema=params['schema'])
#listinoComplessoListinoTable.create(checkfirst=True)
#print "CREATO listino_complesso_listino"

#try:
    #listinoComplessoArticoloPrevalenteTable = Table('listino_complesso_articolo_prevalente',
                                                #params['metadata'],
                                                #autoload=True,
                                                #schema=params['schema'])
    ##print listinoComplessoArticoloPrevalenteTable.columns
    #if "listinoComplessoArticoloPrevalenteTable.id" not in listinoComplessoArticoloPrevalenteTable.columns:
        #print "TABELLA LISTINO_COMPLESSO_ARTICOLO_PREVALENTE GIÀ AGGIORNATA"
    #else:
        #listinoComplessoArticoloPrevalenteTable.drop(checkfirst=True)
        #print "RIMUOVO LA TABELLA LISTINO_COMPLESSO_ARTICOLO_PREVALENTE RIAVVIARE IL PROMOGEST2"
#except:
    #listinoComplessoArticoloPrevalenteTable = Table('listino_complesso_articolo_prevalente',params['metadata'],
            #Column('id',Integer, primary_key=True),
            #Column('id_listino_complesso',Integer),
            #Column('id_listino',Integer),
            #Column('id_articolo',Integer),
            #Column('data_listino_articolo',DateTime),
            #schema=params['schema'],useexisting=True
            #)
    #listinoComplessoArticoloPrevalenteTable.create(checkfirst=True)
    #print "CREATO listino_complesso_articolo_prevalente"
#appLogTable = Table('application_log', params['metadata'], autoload=True, schema=params['mainSchema'])
#schema = params['mainSchema']
#table = schema+".application_log"

#if "application_log.pkid" not in str(appLogTable.columns):
    #comando = 'ALTER TABLE %s ADD COLUMN pkid varchar(100);' % table
    #params['session'].connection().execute(text(comando))
    #comando = "ALTER TABLE %s ALTER COLUMN object TYPE varchar(300);" % table
    #params['session'].connection().execute(text(comando))

#from promogest.dao.ListinoArticolo import ListinoArticolo


#print "CANCELLATE LE VECCHIE ENTRY IN LISTINO ARTICOLO"
#print "CERCO DI CONVERTIRE IL TIPO COLONNA IN DATETIME"
#schema = params['schema']
#tabella = schema+".sconti_vendita_dettaglio"
#tabella2 = schema+".listino_articolo"
#comando ="ALTER TABLE %s ALTER COLUMN data_listino_articolo TYPE time;" %tabella
#comando ="ALTER TABLE %s ALTER COLUMN data_listino_articolo TYPE time;" %tabella2
#params['session'].connection().execute(text(comando))
#print "SE TUTTO E? ANDATO ENE BUON LAVORO"
