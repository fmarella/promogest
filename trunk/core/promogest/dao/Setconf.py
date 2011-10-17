# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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
from Dao import Dao
from promogest.Environment import *


try:
    setconf=Table('setconf', params['metadata'],schema = params['schema'],autoload=True)
except:
    setconf  = Table('setconf', params["metadata"],
            Column('id',Integer,primary_key=True),
            Column('key',String(50), nullable=False),
            Column('description',String(200), nullable=True),
            Column('value',String(2000)),
            Column('section',String(50), nullable=False),
            Column('tipo_section',String(50)),
            Column('tipo',String(50)),
            Column('date', DateTime, nullable=True),
            Column('active', Boolean, default=True),
            Column('visible', Boolean, default=True),
            UniqueConstraint('key', "section"),
            schema = params['schema'])
    setconf.create(checkfirst=True)

class SetConf(Dao):

    def __init__(self, req= None, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "description":
            dic= { k : setconf.c.description.ilike("%"+v+"%")}
        elif k == "value":
            dic= { k : setconf.c.value == v}
        elif k == "body":
            dic= { k : setconf.c.body.ilike("%"+v+"%")}
        elif k == "section":
            dic= { k : setconf.c.section == v}
        elif k == "key":
            dic= { k : setconf.c.key == v}
        elif k == 'searchkey':
            dic = {k:or_(setconf.c.key.ilike("%"+v+"%"),
                        setconf.c.value.ilike("%"+v+"%"),
                        setconf.c.description.ilike("%"+v+"%"))}
        elif k =="active":
            dic = { k :setconf.c.active ==v}
        elif k =="visible":
            dic = { k :setconf.c.visible ==v}
        return  dic[k]

std_mapper = mapper(SetConf, setconf, order_by=setconf.c.key)

bb = SetConf().select(key="articolo_struttura_codice", section="Articoli")
if not bb:
    kbb = SetConf()
    kbb.key = "articolo_struttura_codice"
    kbb.value ="ART000000"
    kbb.section = "Articoli"
    kbb.tipo_section = "Generico"
    kbb.description = "Articolo struttura codice"
    kbb.active = True
    kbb.tipo = "str"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
bb = SetConf().select(key="articolo_codice_upper", section="Articoli")
if not bb:
    kbb = SetConf()
    kbb.key = "articolo_codice_upper"
    kbb.value ="True"
    kbb.section = "Articoli"
    kbb.tipo_section = "Generico"
    kbb.description = "Articolo struttura codice"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
bb = SetConf().select(key="articolo_immagini", section="Articoli")
if not bb:
    kbb = SetConf()
    kbb.key = "articolo_immagini"
    kbb.value ="True"
    kbb.section = "Articoli"
    kbb.tipo_section = "Generico"
    kbb.description = "Articolo visualizzazione immagini"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)


bb = SetConf().select(key="cliente_struttura_codice", section="Clienti")
if not bb:
    kbb = SetConf()
    kbb.key = "cliente_struttura_codice"
    kbb.value ="CLI000000"
    kbb.section = "Clienti"
    kbb.tipo_section = "Generico"
    kbb.description = "Cliente struttura codice"
    kbb.active = True
    kbb.tipo = "str"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
bb = SetConf().select(key="cliente_codice_upper", section="Clienti")
if not bb:
    kbb = SetConf()
    kbb.key = "cliente_codice_upper"
    kbb.value ="True"
    kbb.section = "Clienti"
    kbb.tipo_section = "Generico"
    kbb.description = "Clienti codice upper"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
bb = SetConf().select(key="cliente_nome_cognome", section="Clienti")
if not bb:
    kbb = SetConf()
    kbb.key = "cliente_nome_cognome"
    kbb.value ="False"
    kbb.section = "Clienti"
    kbb.tipo_section = "Generico"
    kbb.description = "Visualizza nome cognome"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)

bb = SetConf().select(key="fornitore_struttura_codice", section="Fornitori")
if not bb:
    kbb = SetConf()
    kbb.key = "fornitore_struttura_codice"
    kbb.value ="FOR000000"
    kbb.section = "Fornitori"
    kbb.tipo_section = "Generico"
    kbb.description = "Fornitori struttura codice"
    kbb.active = True
    kbb.tipo = "str"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
bb = SetConf().select(key="fornitore_codice_upper", section="Fornitori")
if not bb:
    kbb = SetConf()
    kbb.key = "fornitore_codice_upper"
    kbb.value ="True"
    kbb.section = "Fornitori"
    kbb.tipo_section = "Generico"
    kbb.description = "Fornitori codice upper"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
bb = SetConf().select(key="fornitore_nome_cognome", section="Fornitori")
if not bb:
    kbb = SetConf()
    kbb.key = "fornitore_nome_cognome"
    kbb.value ="False"
    kbb.section = "Fornitori"
    kbb.tipo_section = "Generico"
    kbb.description = "Visualizza nome cognome"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)

bb = SetConf().select(key="vettore_struttura_codice", section="Vettori")
if not bb:
    kbb = SetConf()
    kbb.key = "vettore_struttura_codice"
    kbb.value ="VE0000"
    kbb.section = "Vettori"
    kbb.tipo_section = "Generico"
    kbb.description = "Vettori struttura codice"
    kbb.active = True
    kbb.tipo = "str"
    kbb.date = datetime.datetime.now()
    session.add(kbb)

bb = SetConf().select(key="valuta_curr", section="Valuta")
if not bb:
    kbb = SetConf()
    kbb.key = "valuta_curr"
    kbb.value ="€"
    kbb.section = "Valuta"
    kbb.tipo_section = "Generico"
    kbb.description = "Vvaluta"
    kbb.active = True
    kbb.tipo = "str"
    kbb.date = datetime.datetime.now()
    session.add(kbb)

bb = SetConf().select(key="vettore_codice_upper", section="Vettori")
if not bb:
    kbb = SetConf()
    kbb.key = "vettore_codice_upper"
    kbb.value ="True"
    kbb.section = "Vettori"
    kbb.tipo_section = "Generico"
    kbb.description = "Vettori codice upper"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)

if not SetConf().select(key="project_name"):
    key_name = SetConf()
    key_name.key = "project_name"
    key_name.value ="Pg2 WEB"
    key_name.section = "Project"
    key_name.description = " Nome del progetto"
    key_name.active = True
    key_name.date = datetime.datetime.now()
    key_name.persist()
if not SetConf().select(key="subdomain", section="Servizi"):
    key_name = SetConf()
    key_name.key = "subdomain"
    key_name.value ="/siteAdmin/subdomainList"
    key_name.section = "Servizi"
    key_name.description = " Gestione dei sottodomini"
    key_name.active = True
    key_name.date = datetime.datetime.now()
    key_name.persist()
if not SetConf().select(key="uri"):
    key_uri = SetConf()
    key_uri.key = "uri"
    key_uri.value = "http://www.promotux.it"
    key_uri.section = "Project"
    key_uri.description = "HOST DI PARTENZA"
    key_uri.active = True
    key_uri.date = datetime.datetime.now()
    key_uri.persist()
if not SetConf().select(key="cookie_name"):
    key_cookie = SetConf()
    key_cookie.key = "cookie_name"
    key_cookie.value = "janascookie"
    key_cookie.section = "Project"
    key_cookie.description = "Descrizione del cookie"
    key_cookie.active = True
    key_cookie.date = datetime.datetime.now()
    key_cookie.persist()
if not SetConf().select(key="head_title"):
    key_mf = SetConf()
    key_mf.key = "head_title"
    key_mf.value = "PromoTUX - Virtual company - Servizi e soluzioni gestionali per la tua azienda - Open source e Linux - Promotux snc"
    key_mf.section = "Project"
    key_mf.description = "Titolo standar della pagina principale"
    key_mf.active = True
    key_mf.date = datetime.datetime.now()
    key_mf.persist()
if not SetConf().select(key="news_list_number"):
    key_nln = SetConf()
    key_nln.key = "news_list_number"
    key_nln.value = "3"
    key_nln.section = "Project"
    key_nln.description = "Numero di news nella sidebar"
    key_nln.active = True
    key_nln.date = datetime.datetime.now()
    key_nln.persist()
if not SetConf().select(key="smtpserver"):
    key_nln = SetConf()
    key_nln.key = "smtpserver"
    key_nln.value = "smtp.tiscali.it"
    key_nln.section = "Project"
    key_nln.description = "server smtp con cui spedire le email"
    key_nln.active = True
    key_nln.date = datetime.datetime.now()
    key_nln.persist()
if not SetConf().select(key="self_confirm"):
    key_nln = SetConf()
    key_nln.key = "self_confirm"
    key_nln.value = True
    key_nln.section = "Project"
    key_nln.description = "indica se nella registrazione serve l'email don conferma"
    key_nln.active = True
    key_nln.date = datetime.datetime.now()
    key_nln.persist()

COOKIENAME = SetConf().select(key="cookie_name")[0].value

session.commit()
