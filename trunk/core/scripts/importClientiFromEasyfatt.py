# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010,2011 by Promotux
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

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.interfaces import PoolListener
from sqlalchemy.ext.sqlsoup import SqlSoup
from sqlalchemy.interfaces import ConnectionProxy
import csv

"""
    CAMPI CSV CLIENTI Easyfatt:

        0  "Cod."; =  Clienti:string
        1  "Denominazione"; = Clienti:string
        2  "Indirizzo";  =  Clienti:string.  Sede_legale_indirizzo
        3  "Cap"; = Clienti:string Sede_legale_cap
        4  "Città"; Clienti:string Sede_legale_citta
        5  "Prov."; Clienti:string Sede_legale_provincia
        6  "Regione"; Clienti: strig Sede_legale_regione
        7  "Nazione"; Clienti: string  nazione
        8  "Partita Iva"; Clienti :string
        9  "Codice fiscale"; Clienti: string
        10 "Extra 1"; NO
        11 "Extra 2"; NO
        12 "Note";  NO
        13 "Listino";  Cliente integer  id_listino
        14 "Sconti";   CHE VUOL DIRE ....
        15 "Banca";    Clienti id_banca
        16 "Ns Banca"; NO
        17 "Agente"; NO
        18 "Rit. acconto?"; NO
        19 "Pagamento";  id_pagamento
        20 "Fatt. con Iva"; ???  RIFERIMENTO A CLIENTE DETTAGLIO ... Interessante....
        21 "Rif. Persona"; ??? CHE VUOL DIRE ?

        22 "Tel.";  Recapito Telefono
        23 "Cell";  Recapito Cellulare
        24 "Fax";   Recapito Fax
        25 "Desc. Tel. 2";  SU PG NON SERVE
        26 "Tel. 2"; Recapito Telefono
        27 "Desc. Tel. 3";  SU PG NON SERVE
        28 "Tel. 3"; Recapito Telefono
        29 "e-mail";  Recapito Email
        30 "Home page"; Recapito Sito
        31 "Login web"; NO
        32 "Conto reg."; ??????????
        33 "Note doc." ??????????
"""

#PARAMETRI CONNESSIONE:

TIPO = "sqlite" # sqlite o postgresql

# Versione PRO:
AZIENDA = "AziendaPromo"
DB_NAME = "promogest_db"
PORT = "5432"
USER = "promoadmin"
PASSWORD = "admin"
MAINSCHEMA = "promogest2"
HOST = "127.0.0.1"
# Versione ONE
DB_PATH = "/home/mentore/promogest2/"
#File da importare
FILE_CSV = "/home/mentore/clienti_francesco.csv"
DELIMITER = ";"
QUOTECHAR = '"'

#PARAMETRI GENERICI:
USA_CODICE_CLIENTE = True   #  True o False  : Usa il codice cliente dal file csv o usa quello di base del PromoGest

class MyProxy(ConnectionProxy):
    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
        return execute(cursor, statement, parameters, context)

class SetTextFactory(PoolListener):
     def connect(self, dbapi_con, con_record):
         dbapi_con.text_factory = str

class GenericFillData(object):
    def __init__(self):
        self.azienda = AZIENDA
        self.db_name = DB_NAME
        self.port = PORT
        self.tipo = TIPO
        self.user = USER
        self.password = PASSWORD
        self.mainSchema = MAINSCHEMA
        self.host = HOST
        self.file_csv = FILE_CSV
        self.db_path = DB_PATH
        self.connection()

    def connection(self):
        if self.tipo == "postgresql":
            engine = create_engine('postgres:'+'//'+self.user+':'
                                + self.password+ '@'
                                + self.host + ':'
                                + self.port + '/'
                                + self.db_name,
                                encoding='utf-8',
                                convert_unicode=True )
        else:
            self.azienda = None
            self.mainSchema = None
            engine =create_engine("sqlite:///"+self.db_path+"db",listeners=[SetTextFactory()],proxy=MyProxy())
        engine.echo = True
        meta = MetaData(engine)
        self.pg_db_dest = SqlSoup(meta)
        self.pg_db_dest.schema = self.azienda
        self.readFile()

    def readFile(self):
        spamReader = csv.reader(open(self.file_csv), delimiter=';', quotechar='"')
        spamReader.next() # Skip header line.
        self.fillDataContact(spamReader)

    def fillDataContact(self,spamReader):
        for row in spamReader:
            ah = self.pg_db_dest.persona_giuridica.filter_by(codice=row[0]).all()
            if ah:
                continue
            pg = self.pg_db_dest.persona_giuridica()
            pg.codice = row[0]
            pg.ragione_sociale = row[1]
            pg.sede_legale_indirizzo = row[2]
            pg.sede_legale_cap = row[3]
            pg.sede_legale_localita = row[4]
            pg.sede_legale_provincia = row[5]
            pg.nazione = row[7]
            pg.partita_iva = row[8]
            pg.codice_fiscale = row[9]
            sqlalchemy.ext.sqlsoup.Session.add(pg)
            sqlalchemy.ext.sqlsoup.Session.commit()

            cli = self.pg_db_dest.cliente()
            cli.id = pg.id
#            cli.ragione_sociale = row[1]
            sqlalchemy.ext.sqlsoup.Session.add(cli)
            sqlalchemy.ext.sqlsoup.Session.commit()

            if self.tipo =="sqlite":
                iid = None
                forMaxId = self.pg_db_dest.contatto.all()
                if not forMaxId:
                    iid = 1
                else:
                    idss = []
                    for l in forMaxId:
                        idss.append(l.id)
                    iid = (max(idss)) +1
#            cont.id_cliente = cli.id
            cont = self.pg_db_dest.contatto()
            if self.tipo =="sqlite":
                cont.id = iid
            cont.tipo_contatto ="cliente"
            cont.note = row[12]
            sqlalchemy.ext.sqlsoup.Session.add(cont)
            sqlalchemy.ext.sqlsoup.Session.commit()

            concli = self.pg_db_dest.contatto_cliente()
            concli.id = cont.id
            concli.tipo_contatto = "cliente"
            concli.id_cliente = cli.id
            sqlalchemy.ext.sqlsoup.Session.add(concli)
            sqlalchemy.ext.sqlsoup.Session.commit()

            if row[22] and row[22] != "":
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[22]
                _recapiti.tipo_recapito="Telefono"
                _recapiti.id_contatto=cont.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)
                sqlalchemy.ext.sqlsoup.Session.commit()

            if row[23] and row[23] != "":
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[23]
                _recapiti.tipo_recapito="Cellulare"
                _recapiti.id_contatto=cont.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)
                sqlalchemy.ext.sqlsoup.Session.commit()

            if row[24] and row[24] != "":
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[24]
                _recapiti.tipo_recapito="Fax"
                _recapiti.id_contatto=cont.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)
                sqlalchemy.ext.sqlsoup.Session.commit()

            if row[26] and row[26] != "":
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[26]
                _recapiti.tipo_recapito="Telefono"
                _recapiti.id_contatto=cont.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)
                sqlalchemy.ext.sqlsoup.Session.commit()

            if row[28] and row[28] != "":
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[28]
                _recapiti.tipo_recapito="Telefono"
                _recapiti.id_contatto=cont.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)
                sqlalchemy.ext.sqlsoup.Session.commit()

            if row[29] and row[29] != "":
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[29]
                _recapiti.tipo_recapito="Email"
                _recapiti.id_contatto=cont.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)
                sqlalchemy.ext.sqlsoup.Session.commit()

            if row[29] and row[30] != "":
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[30]
                _recapiti.tipo_recapito="Sito"
                _recapiti.id_contatto=cont.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)
                sqlalchemy.ext.sqlsoup.Session.commit()

#    def name(self, data):
#        rowlist = data.split(" ")
#        if len(rowlist) == 4:
#            cognome = rowlist[0] + " " +rowlist[1]
#            nome = rowlist[2] + " " +rowlist[3]
#        elif len(rowlist)==3:
#            cognome = rowlist[0] + " " +rowlist[1]
#            nome = rowlist[2]
#        elif len(rowlist)==2:
#            cognome = rowlist[0]
#            nome = rowlist[1]
#        elif len(rowlist) == 1:
#            cognome = rowlist[0]
#            nome = None
#        elif len(rowlist) >4:
#            cognome = rowlist
#            nome = None
#        return (cognome, nome)


if __name__ == "__main__":
    GenericFillData()
