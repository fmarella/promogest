# -*- coding: utf-8 -*-
# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import pool
from sqlalchemy.ext.sqlsoup import SqlSoup
import csv

class GenericFillData(object):
    def __init__(self):
        self.azienda_destinazione = "latelier"
        self.database = "promogest_db"
        self.port = "5432"
        self.user = "promoadmin"
        self.password = "admin"
        self.host = "localhost"
        self.file_csv = "aliquota_iva.csv"
        self.mainSchema = "promogest2"
        self.connection()

    def connection(self):
        engine = create_engine('postgres:'+'//'+self.user+':'
                            + self.password+ '@'
                            + self.host + ':'
                            + self.port + '/'
                            + self.database,
                            encoding='utf-8',
                            convert_unicode=True )

        engine.echo = True
        meta = MetaData(engine)
        self.pg_db_dest = SqlSoup(meta)
        self.pg_db_dest.schema = self.azienda_destinazione
        self.readFile()
    
    def readFile(self):
        spamReader = csv.reader(open(self.file_csv), delimiter=';', quotechar='"')
        self.fillDataContact(spamReader)
    
    def fillDataContact(self,spamReader):
        for row in spamReader:
            _art = self.pg_db_dest.aliquota_iva()
            _art.id=row[0]
            _art.denominazione_breve=row[1]
            _art.denominazione=row[2]
            _art.percentuale = row[3]
            _art.percentuale_detrazione = row[4]
            _art.descrizione_detrazione = row[5]
            _art.id_tipo = row[6]

            sqlalchemy.ext.sqlsoup.Session.add(_art)
            sqlalchemy.ext.sqlsoup.Session.commit()

        self.pg_db_dest.flush()

if __name__ == "__main__":
    GenericFillData()
