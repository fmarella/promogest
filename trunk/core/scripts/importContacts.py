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
        self.azienda_destinazione = "elisir"
        self.database = "promogest_db"
        self.port = "5432"
        self.user = "promoadmin"
        self.password = "admin"
        self.host = "localhost"
        self.file_csv = "coppola_cli.csv"
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
            _contatti = self.pg_db_dest.contatto()
            nomecognome = self.name(row[1])
            _contatti.tipo_contatto="generico"
            _contatti.nome=nomecognome[1]
            _contatti.cognome=nomecognome[0]

            sqlalchemy.ext.sqlsoup.Session.add(_contatti)
            sqlalchemy.ext.sqlsoup.Session.commit()

            _recapiti = self.pg_db_dest.recapito()
            _recapiti.recapito=row[3]
            _recapiti.tipo_recapito="Indirizzo"
            _recapiti.id_contatto=_contatti.id
            sqlalchemy.ext.sqlsoup.Session.add(_recapiti)

            #sqlalchemy.ext.sqlsoup.Session.commit()
            #self.pg_db_dest.flush()

            _recapiti = self.pg_db_dest.recapito()
            _recapiti.recapito=row[4]
            _recapiti.tipo_recapito="CAP"
            _recapiti.id_contatto=_contatti.id
            sqlalchemy.ext.sqlsoup.Session.add(_recapiti)

            _recapiti = self.pg_db_dest.recapito()
            _recapiti.recapito=row[5]
            _recapiti.tipo_recapito="Citta'"
            _recapiti.id_contatto=_contatti.id
            sqlalchemy.ext.sqlsoup.Session.add(_recapiti)

            _recapiti = self.pg_db_dest.recapito()
            _recapiti.recapito=row[6]
            _recapiti.tipo_recapito="Provincia"
            _recapiti.id_contatto=_contatti.id
            sqlalchemy.ext.sqlsoup.Session.add(_recapiti)

            if row[7] !='':
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[7]
                _recapiti.tipo_recapito="Telefono"
                _recapiti.id_contatto=_contatti.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)

            if row[8] !='':
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[8]
                _recapiti.tipo_recapito="Telefono"
                _recapiti.id_contatto=_contatti.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)

            if row[9] !='':
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[9]
                _recapiti.tipo_recapito="Fax"
                _recapiti.id_contatto=_contatti.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)

            if row[10] !='':
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[10]
                _recapiti.tipo_recapito="Info"
                _recapiti.id_contatto=_contatti.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)

            if row[11] !='':
                _recapiti = self.pg_db_dest.recapito()
                _recapiti.recapito=row[11]
                _recapiti.tipo_recapito="Info"
                _recapiti.id_contatto=_contatti.id
                sqlalchemy.ext.sqlsoup.Session.add(_recapiti)
            sqlalchemy.ext.sqlsoup.Session.commit()
            self.pg_db_dest.flush()

    def name(self, data):
        rowlist = data.split(" ")
        if len(rowlist) == 4:
            cognome = rowlist[0] + " " +rowlist[1]
            nome = rowlist[2] + " " +rowlist[3]
        elif len(rowlist)==3:
            cognome = rowlist[0] + " " +rowlist[1]
            nome = rowlist[2]
        elif len(rowlist)==2:
            cognome = rowlist[0]
            nome = rowlist[1]
        elif len(rowlist) == 1:
            cognome = rowlist[0]
            nome = None
        elif len(rowlist) >4:
            cognome = rowlist
            nome = None
        return (cognome, nome)

    #def maxid(self,data):
        #if data:
            #a = max(rec.id for rec in data)
        #else:
            #a = 1
        #return a



    #categoria_contatto_sequence = Sequence("categoria_contatto_id_seq", schema=params["schema_destinazione"])
    #for rec in v:
        #pg_db_dest.categoria_contatto.insert(id=rec.id,
                                            #denominazione = rec.denominazione)
        #sqlalchemy.ext.sqlsoup.Session.commit()
        #pg_db_dest.flush()
    #maxo = maxid(v)
    #for i in range(0,int(maxo)):
        #params['db_pg'].execute(categoria_contatto_sequence)


    #contatto_sequence = Sequence("contatto_id_seq", schema=params["schema_destinazione"])
    #for rec in v:
        #pg_db_dest.contatto.insert(id=rec.id,
                                    #tipo_contatto=rec.tipo_contatto,
                                    #nome=rec.nome,
                                    #cognome=rec.cognome,
                                    #ruolo=rec.ruolo,
                                    #descrizione=rec.descrizione,
                                    #note=rec.note)
        #sqlalchemy.ext.sqlsoup.Session.commit()
        #pg_db_dest.flush()
    #maxo = maxid(v)
    #for i in range(0,int(maxo)):
        #params['db_pg'].execute(contatto_sequence)


    #recapito_sequence = Sequence("recapito_id_seq", schema=params["schema_destinazione"])
    #for rec in v:
        #if rec.tipo_recapito == "E-Mail": fix = "Email"
        #else: fix = rec.tipo_recapito
        #pg_db_dest.recapito(id=rec.id,
                            #recapito=rec.recapito,
                            #tipo_recapito=fix,
                            #id_contatto=rec.id_contatto)
        #sqlalchemy.ext.sqlsoup.Session.commit()
        #pg_db_dest.flush()
    #maxo = maxid(v)
    #for i in range(0,int(maxo)):
        #params['db_pg'].execute(recapito_sequence)

if __name__ == "__main__":
    GenericFillData()
