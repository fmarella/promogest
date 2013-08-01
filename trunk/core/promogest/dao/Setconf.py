# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

import hashlib
from sqlalchemy import *
from sqlalchemy.orm import *
from Dao import Dao
from promogest.Environment import *
from promogest.lib.utils import orda

try:
    t_setconf=Table('setconf',params['metadata'] ,schema = params['schema'],autoload=True)
except:
    from data.setconf import t_setconf


class SetConf(Dao):

    def __init__(self, req= None, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self, k, v):
        if k == "description":
            dic= { k : t_setconf.c.description.ilike("%"+v+"%")}
        elif k == "value":
            dic= { k : t_setconf.c.value == v}
        elif k == "body":
            dic= { k : t_setconf.c.body.ilike("%"+v+"%")}
        elif k == "section":
            dic= { k : t_setconf.c.section == v}
        elif k == "key":
            dic= { k : t_setconf.c.key == v}
        elif k == 'searchkey':
            dic = {k:or_(t_setconf.c.key.ilike("%"+v+"%"),
                        t_setconf.c.value.ilike("%"+v+"%"),
                        t_setconf.c.description.ilike("%"+v+"%"))}
        elif k =="active":
            dic = { k :t_setconf.c.active ==v}
        elif k =="visible":
            dic = { k :t_setconf.c.visible ==v}
        return  dic[k]

std_mapper = mapper(SetConf, t_setconf,
    properties={
        'description':deferred(t_setconf.c.description),
        'date':deferred(t_setconf.c.date),
    }, order_by=t_setconf.c.key)

allkey = session.query(SetConf.key,SetConf.section).all()
#bb = SetConf().select(key="articolo_struttura_codice", section="Articoli")
a = False
if not ("articolo_struttura_codice","Articoli") in allkey:
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
    a = True
#bb = SetConf().select(key="articolo_codice_upper", section="Articoli")
if not ("articolo_codice_upper", "Articoli") in allkey:
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
    a = True
#bb = SetConf().select(key="articolo_immagini", section="Articoli")
if not ("articolo_immagini", "Articoli") in allkey:
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
    a = True

if not ("cliente_struttura_codice", "Clienti") in allkey:
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
    a = True
if not ("cliente_codice_upper", "Clienti") in allkey:
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
    a = True
if not ("cliente_nome_cognome", "Clienti") in allkey:
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
    a = True

if not ("fornitore_struttura_codice", "Fornitori") in allkey:
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
    a = True

if not ("fornitore_codice_upper", "Fornitori") in allkey:
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
    a = True
if not ("fornitore_nome_cognome", "Fornitori") in allkey:
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
    a = True

if not ("vettore_struttura_codice", "Vettori") in allkey:
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
    a = True

if not ("valuta_curr", "Valuta") in allkey:
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
    a = True

if not ("vettore_codice_upper", "Vettori") in allkey:
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
    a = True

if not ("project_name", "Project") in allkey:
    key_name = SetConf()
    key_name.key = "project_name"
    key_name.value ="Pg2 WEB"
    key_name.section = "Project"
    key_name.description = " Nome del progetto"
    key_name.active = True
    key_name.date = datetime.datetime.now()
    session.add(key_name)
    a = True

if not ("subdomain", "Servizi") in allkey:
    key_name = SetConf()
    key_name.key = "subdomain"
    key_name.value ="/siteAdmin/subdomainList"
    key_name.section = "Servizi"
    key_name.description = " Gestione dei sottodomini"
    key_name.active = True
    key_name.date = datetime.datetime.now()
    session.add(key_name)
    a = True

if not ("uri", "Project") in allkey:
    key_uri = SetConf()
    key_uri.key = "uri"
    key_uri.value = "http://www.promotux.it"
    key_uri.section = "Project"
    key_uri.description = "HOST DI PARTENZA"
    key_uri.active = True
    key_uri.date = datetime.datetime.now()
    session.add(key_uri)
    a = True

if not ("cookie_name", "Project") in allkey:
    key_cookie = SetConf()
    key_cookie.key = "cookie_name"
    key_cookie.value = "janascookie"
    key_cookie.section = "Project"
    key_cookie.description = "Descrizione del cookie"
    key_cookie.active = True
    key_cookie.date = datetime.datetime.now()
    session.add(key_cookie)
    a = True

if not ("head_title", "Project") in allkey:
    key_mf = SetConf()
    key_mf.key = "head_title"
    key_mf.value = "PromoTUX - Virtual company - Servizi e soluzioni gestionali per la tua azienda - Open source e Linux - Promotux snc"
    key_mf.section = "Project"
    key_mf.description = "Titolo standar della pagina principale"
    key_mf.active = True
    key_mf.date = datetime.datetime.now()
    session.add(key_mf)
    a = True

if not ("news_list_number", "Project") in allkey:
    key_nln = SetConf()
    key_nln.key = "news_list_number"
    key_nln.value = "3"
    key_nln.section = "Project"
    key_nln.description = "Numero di news nella sidebar"
    key_nln.active = True
    key_nln.date = datetime.datetime.now()
    session.add(key_nln)
    a = True

if not ("smtpserver", "Project") in allkey:
    key_nln = SetConf()
    key_nln.key = "smtpserver"
    key_nln.value = "smtp.tiscali.it"
    key_nln.section = "Project"
    key_nln.description = "server smtp con cui spedire le email"
    key_nln.active = True
    key_nln.date = datetime.datetime.now()
    session.add(key_nln)
    a = True

if not ("self_confirm", "Project") in allkey:
    key_nln = SetConf()
    key_nln.key = "self_confirm"
    key_nln.value = True
    key_nln.section = "Project"
    key_nln.description = "indica se nella registrazione serve l'email don conferma"
    key_nln.active = True
    key_nln.date = datetime.datetime.now()
    session.add(key_nln)
    a = True

if not ("rotazione_primanota", "Primanota") in allkey:
    kee = SetConf()
    kee.key = "rotazione_primanota"
    kee.value ="mensile"
    kee.section = "Primanota"
    kee.tipo_section = "Generico"
    kee.description = "Gestione della creazione della prima nota, valori ammessi, MESE, SETTIMANA, TRIMESTRE"
    kee.active = True
    kee.date = datetime.datetime.now()
    session.add(kee)
    a = True

if not ("install_code", "Master") in allkey:
    kmm = SetConf()
    kmm.key = "install_code"
    kmm.value =str(hashlib.sha224("aziendapromo"+orda("aziendapromo")).hexdigest())
    kmm.section = "Master"
    kmm.description = "codice identificativo della propria installazione"
    kmm.tipo_section = "General"
    kmm.tipo = "ONE BASIC"
    kmm.active = True
    kmm.date = datetime.datetime.now()
    session.add(kmm)
    a = True

if not ("altezza_logo", "Documenti") in allkey:
    koo = SetConf()
    koo.key = "altezza_logo"
    koo.value ="110"
    koo.section = "Documenti"
    koo.description = "altezza logo documento"
    koo.tipo_section = "Generico"
    koo.active = True
    koo.date = datetime.datetime.now()
    session.add(koo)
    a = True

if not ("larghezza_logo", "Documenti") in allkey:
    kpp = SetConf()
    kpp.key = "larghezza_logo"
    kpp.value ="300"
    kpp.section = "Documenti"
    kpp.description = "larghezza logo documento"
    kpp.tipo_section = "Generico"
    kpp.active = True
    kpp.date = datetime.datetime.now()
    session.add(kpp)
    a = True

if not ("separatore_numerazione", "Documenti") in allkey:
    kpp = SetConf()
    kpp.key = "separatore_numerazione"
    kpp.value ="/"
    kpp.section = "Documenti"
    kpp.description = "separatore numerazione"
    kpp.tipo_section = "Generico"
    kpp.active = True
    kpp.date = datetime.datetime.now()
    session.add(kpp)
    a = True


if not ("ricerca_per", "Documenti") in allkey:
    krr = SetConf()
    krr.key = "ricerca_per"
    krr.value ="codice"
    krr.section = "Documenti"
    krr.description = "Preimposta un tipo di ricerca Valori possibili:(codice,descrizione,codice_a_barre,codice_articolo_fornitore "
    krr.tipo_section = "Generico"
    krr.active = True
    krr.visible = True
    krr.date = datetime.datetime.now()
    session.add(krr)
    a = True

if not ("cartella_predefinita", "General") in allkey:
    krr = SetConf()
    krr.key = "cartella_predefinita"
    krr.value = documentsDir
    krr.section = "General"
    krr.description = "Cartella di salvataggio predefinita"
    krr.tipo_section = "Generico"
    krr.active = True
    krr.visible = True
    krr.date = datetime.datetime.now()
    session.add(krr)
    a = True

if not ("gestione_totali_mercatino", "General") in allkey:
    krr = SetConf()
    krr.key = "gestione_totali_mercatino"
    krr.value = "False"
    krr.section = "General"
    krr.description = "Gestione totali mercatino"
    krr.tipo_section = "Generico"
    krr.active = True
    krr.tipo = "bool"
    krr.visible = True
    krr.date = datetime.datetime.now()
    session.add(krr)
    a = True

if not ("color_base", "Documenti") in allkey:
    kss = SetConf()
    kss.key = "color_base"
    kss.value ="#F9FBA7"
    kss.section = "Documenti"
    kss.description = "Preimposta il colore di base "
    kss.tipo_section = "Generico"
    kss.tipo = "Colore"
    kss.active = True
    kss.date = datetime.datetime.now()
    session.add(kss)
    a = True

if not ("color_text", "Documenti") in allkey:
    ktt = SetConf()
    ktt.key = "color_text"
    ktt.value ="black"
    ktt.section = "Documenti"
    ktt.description = "Preimposta il colore del testo "
    ktt.tipo_section = "Generico"
    ktt.tipo = "Colore"
    ktt.active = True
    ktt.date = datetime.datetime.now()
    session.add(ktt)
    a = True

if not ("feed", "Feed") in allkey:
    kuu = SetConf()
    kuu.key = "feed"
    kuu.value = "True"
    kuu.section = "Feed"
    kuu.description = "Notizie nella home"
    kuu.tipo_section = "Generico"
    kuu.active = True
    kuu.tipo = "bool"
    kuu.date = datetime.datetime.now()
    session.add(kuu)
    a = True

#if not ("smtpserver", "Smtp") in allkey:
    #kvv = SetConf()
    #kvv.key = "smtpserver"
    #kvv.value =""
    #kvv.section = "Smtp"
    #kvv.tipo_section = "Generico"
    #kvv.description = "server per l'invio della posta"
    #kvv.active = True
    #kvv.date = datetime.datetime.now()
    #session.add(kvv)

if not ("emailmittente", "Smtp") in allkey:
    kzz = SetConf()
    kzz.key = "emailmittente"
    kzz.value =""
    kzz.section = "Smtp"
    kzz.tipo_section = "Generico"
    kzz.description = "Email del mittente"
    kzz.active = True
    kzz.tipo = "str"
    kzz.date = datetime.datetime.now()
    session.add(kzz)
    a = True

if not ("multilinealimite", "Multilinea") in allkey:
    kaa = SetConf()
    kaa.key = "multilinealimite"
    kaa.value ="60"
    kaa.section = "Multilinea"
    kaa.tipo_section = "Generico"
    kaa.description = "Gestione dei multilinea nei documenti"
    kaa.active = True
    kaa.tipo = "int"
    kaa.date = datetime.datetime.now()
    session.add(kaa)
    a = True

if not ("decimals", "Numbers") in allkey:
    kbb = SetConf()
    kbb.key = "decimals"
    kbb.value ="3"
    kbb.section = "Numbers"
    kbb.tipo_section = "Generico"
    kbb.description = "Gestione dei decimali"
    kbb.active = True
    kbb.tipo = "int"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
    a = True

if not ("batch_size", "Numbers") in allkey:
    kcc = SetConf()
    kcc.key = "batch_size"
    kcc.value ="15"
    kcc.section = "Numbers"
    kcc.tipo_section = "Generico"
    kcc.description = "Gestione dei batchSize"
    kcc.active = True
    kcc.tipo = "int"
    kcc.date = datetime.datetime.now()
    session.add(kcc)
    a = True

if not ("combo_column", "Numbers") in allkey:
    kdd = SetConf()
    kdd.key = "combo_column"
    kdd.value ="3"
    kdd.section = "Numbers"
    kdd.tipo_section = "Generico"
    kdd.description = "Gestione dei combo_column cioè le colonne nelle combobox"
    kdd.active = True
    kdd.tipo = "int"
    kdd.date = datetime.datetime.now()
    session.add(kdd)
    a = True

if not ("zeri_in_riga", "Stampa") in allkey:
    kuu = SetConf()
    kuu.key = "zeri_in_riga"
    kuu.value =""
    kuu.section = "Stampa"
    kuu.description = "Visualizza gli zeri nelle righe documento"
    kuu.tipo_section = "Generico"
    kuu.active = False
    kuu.tipo = "bool"
    kuu.date = datetime.datetime.now()
    session.add(kuu)
    a = True

if not ("zeri_in_totali", "Stampa") in allkey:
    kuu1 = SetConf()
    kuu1.key = "zeri_in_totali"
    kuu1.value =""
    kuu1.section = "Stampa"
    kuu1.description = "Visualizza gli zeri nei totali"
    kuu1.tipo_section = "Generico"
    kuu1.active = False
    kuu1.tipo = "bool"
    kuu1.date = datetime.datetime.now()
    session.add(kuu1)
    a = True

if not ("gestione_lotti", "General") in allkey:
    krr = SetConf()
    krr.key = "gestione_lotti"
    krr.value = "False"
    krr.section = "General"
    krr.description = "Gestione lotti e scadenze"
    krr.tipo_section = "Generico"
    krr.active = True
    krr.tipo = "bool"
    krr.visible = True
    krr.date = datetime.datetime.now()
    session.add(krr)
    a = True

if not ("fix_riga_movimento", "General") in allkey:
    kbb = SetConf()
    kbb.key = "fix_riga_movimento"
    kbb.value ="False"
    kbb.section = "General"
    kbb.tipo_section = "Generico"
    kbb.description = "Sposta i dati su rigamov forni riga mov vendita"
    kbb.active = True
    kbb.tipo = "bool"
    kbb.date = datetime.datetime.now()
    session.add(kbb)
    a = True

if a:
    session.commit()
