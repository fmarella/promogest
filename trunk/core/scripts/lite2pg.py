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

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.exc import *
from sqlsoup import SQLSoup

from promogest.Environment import startdir, MyProxy
#[Database_source]
tipodb_source = "sqlite"


#[Database_dest]
tipodb_dest = "mysql"
database_dest = "aziendaciccio"
host_dest = "192.168.1.3"
user_dest = "promoadmin"
password_dest = "admin"
port_dest = "3306"
azienda_dest = "aziendaciccio"
conpromogest2 = "yes"


engine_source = create_engine("sqlite:///" + startdir() + "db", encoding='utf-8', proxy=MyProxy())
print engine_source
if tipodb_dest == "mysql":
    from sqlalchemy.pool import NullPool
    engine_dest = create_engine("mysql+mysqldb://" + user_dest + ":" + \
                                        password_dest + "@" + host_dest + ":" + port_dest +\
                                        "/" + database_dest + "?charset=utf8",
                                        poolclass=NullPool)

db_source = SQLSoup(engine_source)
db_dest =  SQLSoup(engine_dest)


#Session_source = sessionmaker(bind=engine_source)
#session_source = Session()
session_source = db_source.session
session_dest = db_dest.session
#Session_dest = sessionmaker(bind=engine_dest)
#session_dest = Session()

meta_source = MetaData()
meta_source.reflect(bind=engine_source)
meta_dest = MetaData()
meta_dest.reflect(bind=engine_dest)

# TODO: Se la tabella non viene trovata, venga creata usando la dir data

for m in reversed(meta_dest.sorted_tables):
    print "DA PULIRE",meta_dest.sorted_tables.index(m),"/",len(meta_dest.sorted_tables),  m
    #d_dest = db_dest.entity(str(m)).all()
    try:
        db_dest.entity(str(m)).delete()
        db_dest.commit()
    except:
        db_dest.rollback()
        if str(m).strip() in ["famiglia_articolo"]:
            d_dest = db_dest.entity(str(m)).all()
            for k in reversed(d_dest):
                db_dest.delete(k)
                db_dest.commit()




for t in meta_source.sorted_tables:
    print "SORGENTE",meta_source.sorted_tables.index(t),"/",len(meta_source.sorted_tables), str(t).strip()
    if str(t).strip() not in ["sqlite_stat1", "section_user","app_log", "feed", "spesa", "provincia", "cart", "chiavi_primarie_log", "static_page", "articolo_associato", "static_menu", "credit_card_type","migration_tmp", "account_email", "pos","riga_prima_nota"]:
        daos_source = db_source.entity(str(t)).all()
        #daos_dest = db_dest.entity(str(t)).all()
        print " Nella tabella ci sono",len(daos_source)
        for dao_s  in daos_source:
            #print "RIGA",daos_source.index(dao_s),"/",len(daos_source), str(t).strip()
            #if dao_s in daos_dest:
                #print " ESISTE"
                #continue
            #else:
                #print "SO", dao_s
                #try:
                #dd = None
                #if str(t).strip() in ["contatto_cliente", "contatto_fornitore","contatto_magazzino", "contatto"]:
                    ##print "DE C", db_dest.entity(str(t)).get((dao_s.id, dao_s.tipo_contatto))
                    #dd = db_dest.entity(str(t)).get((dao_s.id, dao_s.tipo_contatto))
                #elif str(t).strip() in ["listino_articolo"]:
                    #pass
                    ##print "SO LART", dao_s
                #elif str(t).strip() in ["informazioni_fatturazione_documento"]:
                    #dd = db_dest.entity(str(t)).get((dao_s.id_fattura, dao_s.id_ddt))
                #elif str(t).strip() in ["informazioni_fatturazione_documento"]:
                    #dd = db_dest.entity(str(t)).get((dao_s.id_fattura, dao_s.id_ddt))
                #elif str(t).strip() in ["roleaction"]:
                    #dd = db_dest.entity(str(t)).get((dao_s.id_role, dao_s.id_action))
                #elif str(t).strip() in ["listino_magazzino"]:
                    #dd = db_dest.entity(str(t)).get((dao_s.id_listino, dao_s.id_magazzino))
                #elif str(t).strip() in ["listino"]:
                    #pass
                #elif str(t).strip() in ["setting"]:
                    #dd = db_dest.entity(str(t)).get(dao_s.key)
                #elif str(t).strip() in ["tipo_recapito", "operazione"]:
                    #dd = db_dest.entity(str(t)).get(dao_s.denominazione)
                #elif str(t).strip() in ["azienda"]:
                    #dd = db_dest.entity(str(t)).get(dao_s.schemaa)
                #else:
                    ##print "DE", db_dest.entity(str(t)).get(dao_s.id)
                    #dd = db_dest.entity(str(t)).get(dao_s.id)
                #if dd:
                    #db_dest.delete(dd)
                    #db_dest.commit()
                #except:
                    #print "cancellazione RIGA non riuscita"
                    #print "RIMUOVO TUTTA LA TABELLA"
                    #for gg in daos_dest:
                        #if gg:
                            #try:
                                #db_dest.delete(gg)
                                #db_dest.commit()
                                #print "E LIMINATO RECORD "
                            #except:
                                #print "SEMPLICE EXCEPT POI DA TOGLIERE"
                    #print "RILANCIARE"
                    #python = sys.executable
                    #os.execl(python, python, * sys.argv)
                #try:
            a = db_dest.entity(str(t))()
            #except:
                #print " NON SONO RIUSCITO A ISTANZIARE LA TABELLA", t

            for k in dao_s.c:
                c = getattr(dao_s,k.name)
                setattr(a,k.name,c)
            session_dest.add(a)
            try:
                db_dest.commit()
            except Exception as e:
                print "QUESTO ERRORE:", e
                db_dest.rollback()
                continue

# chiusura con tabelle anomale
rpn_s = db_source.riga_prima_nota.all()
#rpn_d = db_dest.riga_prima_nota.all()
for d_s  in rpn_s:
    a = db_dest.riga_prima_nota()
    for k in d_s.c:
        c = getattr(d_s,k.name)
        setattr(a,k.name,c)
    session_dest.add(a)
db_dest.commit()
print " FINITO TUTTO"
