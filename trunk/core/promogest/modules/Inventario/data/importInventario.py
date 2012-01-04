# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

#    This file is part of Promogest.

#    Promogest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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
from sqlalchemy import pool
from sqlalchemy.ext.sqlsoup import SqlSoup
import csv

AZIENDA_DESTINAZIONE = "elisir"
DATABASE = "promogest_db"
PORT = "5432"
USER = "promoadmin"
PASSWORD = "admin"
HOST = "192.168.1.101"
FILE_CSV = "inv_2010_gradisca01_def.csv"
MAINSCHEMA = "promogest2"
DELIMITER = ","
QUOTECHAR = '"'

class GenericFillData(object):
    def __init__(self):
        """ QUESTO script permette di importare la tabella inventario così come
            esportata dal modulo stesso. Il funzionamento è semplice:
            si lancia lo script con "python nomescript" avendo cura che
            il file csv si trovi nella stessa cartella dello script stesso

            schema csv :
               riga = ('Codice, Descrizione, Quantita\', Valore unitario, U.M., ' +
                    'Codice a barre, Famiglia, Categoria,Anno ,idMagazzino , idArticolo ,data_aggiornamento\n')
            schema tabella:
            anno ,id_magazzino , id_articolo , quantita , valore_unitario,data_aggiornamento
        """
        self.connection()

    def connection(self):
        engine = create_engine('postgres:'+'//'+USER+':'
                            + PASSWORD+ '@'
                            + HOST + ':'
                            + PORT + '/'
                            + DATABASE,
                            encoding='utf-8',
                            convert_unicode=True )

        engine.echo = True
        meta = MetaData(engine)
        self.pg_db_dest = SqlSoup(meta)
        self.pg_db_dest.schema = AZIENDA_DESTINAZIONE
        self.readFile()

    def readFile(self):
        spamReader = csv.reader(open(FILE_CSV), delimiter=DELIMITER, quotechar=QUOTECHAR)
        self.fillDataContact(spamReader)

    def fillDataContact(self,spamReader):
        for row in spamReader:
            quantita = float(row[2].strip().replace(",","."))
            if quantita >0:
                _field = self.pg_db_dest.inventario()
                _field.anno=int(row[8])
                _field.id_magazzino = int(row[9])
                _field.id_articolo = int(row[10])

                _field.quantita = quantita
                _field.valore_unitario = float(row[3].strip().replace(",","."))
                _field.data_aggiornamento = row[11] or None
                sqlalchemy.ext.sqlsoup.Session.add(_field)
                sqlalchemy.ext.sqlsoup.Session.commit()

#        self.pg_db_dest.flush()

if __name__ == "__main__":
    GenericFillData()
