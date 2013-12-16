#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

import sys
import os
path = ".."
if path not in sys.path:
    sys.path.append(path)

import logging
import logging.handlers
import smtplib
import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.interfaces import PoolListener
from sqlalchemy.exc import *
from sqlalchemy.interfaces import ConnectionProxy
from sqlsoup import SQLSoup
from sqlalchemy.pool import NullPool
#from promogest.Environment import startdir, MyProxy
from promogest.lib.utils import timeit , messageInfo

""" ***********************************************************
 AREA DI CONFIGURAZIONE:
 Consiglio di fare una copia di questo file e di usare quella,
 come prima cosa andranno correttamente configurati i parametri del
 db di origine e di quello di destinazione

 tipodb_source e tipodb_dest possono essere sqlite (ONE) , mysql (MY)  o postgresql (PRO)
 port_source e port_dest sono 3306 per mysql e 5432 per postgresql

 *******************************************************************"""

"""      [Database_source]     """
tipodb_source = "mysql"
database_source = "aziendaciccio"
host_source = "192.168.1.3"
user_source = "promoadmin"
password_source = "admin"
port_source = "3306"
azienda_source = "aziendaciccio"

"""      [Database_dest]       """
tipodb_dest = "postgresql"
database_dest = "aziendaciccio_db"
host_dest = "192.168.1.3"
user_dest = "promoadmin"
password_dest = "admin"
port_dest = "5432"
azienda_dest = "aziendaciccio"


def getConfigureDir(company='__default__'):
    """ Tests if another configuration folder was indicated """
    default='promogest2'
    if company != '__default__' and company is not None:
        default = os.path.join('promogest2', company)
    return default

def startdir():
    startDir = getConfigureDir()
    promogestStartDir = os.path.expanduser('~') + os.sep + startDir + os.sep
    return promogestStartDir

def sanitazer(c, tipo):
    """ funzione di controllo e pulizia dei tipi
    per il momento gestiamo i bool
    """
    #print "CCC", c, tipo, type(tipo), "TINYINT" in str(tipo)
    if str(tipo) == "BOOLEAN" or "TINYINT" in str(tipo):
        #print " SONO PASSATO"
        if c == 0 or c =="0":
            return False
        elif c == 1 or c == "1":
            return True
        else:
            return c
    else:
        return c


# **************  DATABASE DI ORIGINE
if tipodb_source == "sqlite":
    engine_source = create_engine("sqlite:///" + startdir() + "db", encoding='utf-8')
    print " MIGRAZIONE DA SQLITE A "
elif tipodb_source == "mysql":
    print "MIGRAZIONE DA MYSQL A "
    engine_source = create_engine("mysql+mysqldb://" + user_source + ":" + \
                                        password_source + "@" + host_source + ":" + port_source +\
                                        "/" + database_source + "?charset=utf8",
                                        poolclass=NullPool)
elif tipodb_source == "postgresql":
    print "MIGRAZIONE DA POSTGRESQL A "
    import psycopg2
    a = psycopg2.connect(user=user_source, host=host_source, port=port_source,
                            password=password_source, database=database_source)
    engine_dest = create_engine('postgresql://', creator=a,
                                convert_unicode=True,
                                encoding='utf-8',

                                poolclass=NullPool)
else:
    print "ORIGINE MIGRAZIONE NON RICONOSCIUTO"

# ****************** DATABASE DI DESTINAZIONE
if tipodb_dest == "mysql":
    print " MYSQL ...."
    engine_dest = create_engine("mysql+mysqldb://" + user_dest + ":" + \
                                        password_dest + "@" + host_dest + ":" + port_dest +\
                                        "/" + database_dest + "?charset=utf8",
                                        poolclass=NullPool)
elif tipodb_dest == "sqlite":
    print "SQLITE....."
elif tipodb_dest == "postgresql":
    print "POSTGRESQL......"
    engine_dest = create_engine('postgresql+psycopg2://' +
                                    user_dest + ":" +
                                    password_dest + "@" +
                                    host_dest + ":" +
                                    port_dest + "/" +
                                    database_dest,
                                convert_unicode=True,
                                encoding='utf-8',
                                poolclass=NullPool)
else:
    print " DESTINAZIONE NON RICONOSCIUTA"


db_source = SQLSoup(engine_source)
db_dest =  SQLSoup(engine_dest)
#db_dest.schema = azienda_dest
#db_dest.schema = "promogest2"
#engine_dest.echo=True

meta_source = MetaData()
meta_source.reflect(bind=engine_source)

if tipodb_dest == "postgresql":
    meta_dest = MetaData()
    meta_dest_main = MetaData()
    meta_dest_main.reflect(bind=engine_dest, schema="promogest2")
    meta_dest.reflect(bind=engine_dest, schema=azienda_dest)
    tbl_main =  [x.split(".")[1] for x in meta_dest_main.tables]
    tbl = [x.split(".")[1] for x in meta_dest.tables]
else:
    meta_dest = MetaData()
    meta_dest.reflect(bind=engine_dest)
    tbl = [x for x in meta_dest.tables]


session_source = db_source.session
session_dest = db_dest.session
#print meta_dest.tables, meta_dest_main.tables

#raise
@timeit
def pulisciTabelleMain():
    for m in reversed(meta_dest_main.sorted_tables):
        print "DA PULIRE",meta_dest_main.sorted_tables.index(m),"/",len(meta_dest_main.sorted_tables),  m
        db_dest.schema = "promogest2"
        db_dest.entity(str(m).split(".")[1]).delete()
        db_dest.commit()
# TODO: Se la tabella non viene trovata, venga creata usando la dir data

@timeit
def pulisciTabelle():
    for m in reversed(meta_dest.sorted_tables):
        print "DA PULIRE",meta_dest.sorted_tables.index(m),"/",len(meta_dest.sorted_tables),  m #, m.columns
        try:
            if tipodb_dest =="postgresql":
                if str(m).split(".")[0] == azienda_dest:
                    db_dest.schema = azienda_dest
                    db_dest.entity(str(m).split(".")[1]).delete()
                    db_dest.commit()
            else:
                db_dest.schema = azienda_dest
                db_dest.entity(str(m)).delete()
                db_dest.commit()

        except:
            db_dest.rollback()
            if str(m) == "testata_documento":
                rows = db_dest.entity(str(m)).filter(db_dest.testata_documento.id_primo_riferimento !="None").all()
                for r in rows:
                    db_dest.delete(r)
                    db_dest.commit()
                db_dest.entity(str(m)).delete()
                db_dest.commit()
            print " PULISCO MA USO LA MODALITA' LENTA "
            d_dest = db_dest.entity(str(m)).all()
            for k in reversed(d_dest):
                #print k
                db_dest.delete(k)
                db_dest.commit()


@timeit
def spostaDati():
    ritestare = []
    for t in meta_source.sorted_tables:
        print "\nSORGENTE",meta_source.sorted_tables.index(t),"/",len(meta_source.sorted_tables), str(t).strip() ,"\n"
        if str(t).strip() not in ["sqlite_stat1", "section_user","app_log", "feed", "spesa", "provincia", "cart", "chiavi_primarie_log", "static_page", "articolo_associato", "static_menu", "credit_card_type","migration_tmp", "account_email", "pos", "riga_prima_nota"]:
            if str(t).strip() == "testata_documento":
                nope = []
                rows = db_source.entity(str(t)).filter(db_source.testata_documento.id_primo_riferimento !="None").all()
                #print " ROWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWS", len(rows)
                for r in rows:
                    print r.id, r.id_primo_riferimento
                    dao_principale = db_source.entity(str(t)).get(r.id_primo_riferimento)
                    #print "DAO PRINCIPALE", dao_principale
                    m = db_dest.entity(str(t))()
                    for k in dao_principale.c:
                        c = getattr(dao_principale,k.name)
                        c = sanitazer(c, k.type)
                        setattr(m,k.name,c)
                    session_dest.add(m)
                    try:
                        db_dest.commit()
                    except:
                        db_dest.rollback()
                    nope.append(m)
            daos_source_count = db_source.entity(str(t)).count()
            batchSize = 200
            blocchi = daos_source_count/200
            #print daos_source_count, blocchi
            x = 0
            offset = 0
            while offset < daos_source_count+batchSize:
                print daos_source_count, daos_source_count-offset
                daos_source = db_source.entity(str(t)).limit(batchSize).offset(offset).all()
                offset += batchSize
                #print daos_source
                #daos_source = db_source.entity(str(t)).all()
                #daos_dest = db_dest.entity(str(t)).all()
                #print " Nella tabella ci sono",len(daos_source)
                docu_pri_ref = []
                if str(t) in["testata_documento"]:
                    for dao_s  in daos_source:
                        if dao_s not in nope:
                            a = db_dest.entity(str(t))()
                            for k in dao_s.c:
                                c = getattr(dao_s,k.name)
                                c = sanitazer(c, k.type)
                                setattr(a,k.name,c)
                            session_dest.add(a)
                            #try:
                    db_dest.commit()
                            #except:
                                #db_dest.rollback()
                                #print " NON SALVABILE", a
                #elif  str(t) in["articolo"]:
                    #for dao_s  in daos_source:
                        #a = db_dest.entity(str(t))()
                        #for k in dao_s.c:
                            #c = getattr(dao_s,k.name)
                            #c = sanitazer(c, k.type)
                            #setattr(a,k.name,c)
                        #session_dest.add(a)
                        #db_dest.commit()
                else:
                    for dao_s  in daos_source:
                        #if daos_source.index(dao_s)%250 == 0:
                            ##print "RIMANGONO", len(daos_source)-daos_source.index(dao_s), "righe", str(t).strip() ,"su", len(daos_source)
                            #db_dest.commit()
                        a = db_dest.entity(str(t))()
                        for k in dao_s.c:
                            c = getattr(dao_s,k.name)
                            c = sanitazer(c, k.type)
                            setattr(a,k.name,c)
                        session_dest.add(a)
                    try:
                        db_dest.commit()
                    except Exception as e:
                        print "QUESTO ERRORE:", e
                        db_dest.rollback()
                        ritestare.append(a)
                        continue
            if str(t) in["testata_documento"]:
                daos_source_countt = db_source.riga_prima_nota.count()
                batchSizee = 200
                blocchii = daos_source_countt/200
                x = 0
                offsett = 0
                print " SIAMO IN RIGA PRIMA NOTA"
                while offsett < daos_source_countt+batchSizee:
                    print daos_source_countt, daos_source_countt-offsett
                    daos_sourcee = db_source.riga_prima_nota.limit(batchSizee).offset(offsett).all()
                    offsett += batchSizee
                    for dao_s  in daos_sourcee:
                        a = db_dest.riga_prima_nota()
                        for k in dao_s.c:
                            c = getattr(dao_s,k.name)
                            c = sanitazer(c, k.type)
                            setattr(a,k.name,c)
                        session_dest.add(a)
                    db_dest.commit()
    if ritestare:
        print "ADESSO RIPROVIAMO I RITESTARE", len(ritestare)
        for r in ritestare:
            session_dest.add(r)
            db_dest.commit()
    else:
        print " ABBIAMO FINITO LA MIGRAZIONE.... OLE'"
@timeit
def syncaSequence():
    for s in tbl:
        try:
            print "TABELLA SEQUENCE", s
            daos_source = db_source.entity(str(s)).order_by('-id').first()
            try:
                nextid = db_dest.connection().execute("select setval("+"'"+azienda_dest+"."+ str(s)+'_id_seq'+"',"+ str(daos_source.id) +')')
            except Exception as r:
                #print "ERRORE SEQUENCE STD", r
                db_dest.rollback()
        except:
            print "NON HA UN ID E DI CONSEGUENZA NESSUNA SEQUENCE", s
    for s in tbl_main:
        try:
            print "TABELLA SEQUENCE MAIN", s
            daos_source = db_source.entity(str(s)).order_by('-id').first()
            try:
                nextid = db_dest.connection().execute("select setval("+"'"+"promogest2"+"."+ str(s)+'_id_seq'+"',"+ str(daos_source.id) +')')
            except Exception as r:
                #print "ERRORE SEQUENCE STD", r
                db_dest.rollback()
        except:
            print "NON HA UN ID E DI CONSEGUENZA NESSUNA SEQUENCE", s
    print " FINITO TUTTO"

pulisciTabelle()
if tipodb_dest == "postgresql":
    pulisciTabelleMain()
spostaDati()
if tipodb_dest == "postgresql":
    syncaSequence()

tabelle = [ "access",
            "action",
            "agente",
            "anagrafica_secondaria",
            "azienda",
            "categoria_articolo",
            "categoria_cliente",
            "categoria_contatto",
            "informazioni_contabili_documento",
            "informazioni_fatturazione_documento",
            "testata_documento",
            "cliente",
            "cliente_categoria_cliente",
            "cliente_variazione_listino",
            "codice_a_barre_articolo",
            "contatto",
            "contatto_anagraficasecondaria",
            "contatto_azienda",
            "contatto_categoria_contatto",
            "contatto_cliente",
            "contatto_magazzino",
            "destinazione_merce",
            "famiglia_articolo",
            "banche_azienda",
            "banca",
            "categoria_fornitore",
            "fornitore",
            "fornitura",
            "image",
            "imballaggio",
            "immagine",
            "inventario",
            "language",
            "listino",
            "listino_articolo",
            "listino_categoria_cliente",
            "listino_complesso_articolo_prevalente",
            "listino_complesso_listino",
            "listino_magazzino",
            "magazzino",
            "multiplo",
            "numero_lotto_temp",
            "operazione",
            "pagamento",
            "personagiuridica_personagiuridica",
            "persona_giuridica",
            "promemoria",
            "recapito",
            "regione",
            "contatto_fornitore",
            "riga",
            "riga_commessa",
            "riga_documento",
            "riga_movimento",
            "riga_movimento_fornitura",
            "riga_primanota_testata_documento_scadenza",
            "riga_prima_nota",
            "ritenuta_acconto_riga",
            "role",
            "roleaction",
            "sconti_vendita_dettaglio",
            "sconti_vendita_ingrosso",
            "sconto",
            "sconto_fornitura",
            "sconto_riga_documento",
            "sconto_riga_movimento",
            "sconto_testata_documento",
            "setconf",
            "setting",
            "slafile_immagine",
            "sla_file",
            "stadio_commessa",
            "stato_articolo",
            "stoccaggio",
            "testata_commessa",

            "testata_documento_scadenza",
            "testata_movimento",
            "testata_prima_nota",
            "tipo_aliquota_iva",
            "tipo_recapito",
            "unita_base",
            "utente",
            "utente_immagine",
            "variazione_listino",
            "vettore",
            "articolo",
            "articolo_immagine",
            "articolo_kit",
            "aliquota_iva",
]
