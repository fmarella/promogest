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

import datetime
from decimal import *
from promogest.lib.page import Page
from promogest.dao.Articolo import Articolo, getNuovoCodiceArticolo
from promogest.dao.FamigliaArticolo import FamigliaArticolo
from promogest.dao.CategoriaArticolo import CategoriaArticolo
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.Imballaggio import Imballaggio
from promogest.dao.UnitaBase import UnitaBase
from promogest.dao.StatoArticolo import StatoArticolo
from promogest.lib.webutils import *

def anagraficaArticolo(req, action=None):
    """
    Funzione di gestione delle preview
    """
    def _list_(req, action=None):
        """ """
        fk_denominazione = None
        fk_produttore = None
        fk_codice = None
        fk_codice_a_barre = None
        fk_codice_art_fornitore = None
        fk_id_famiglia_articolo = None
        fk_id_categoria_articolo = None
        fk_id_stato_articolo = None
        fk_elminati = True
        if req.form.to_dict():
            fk_denominazione = req.form.get("denominazione")
            fk_produttore = req.form.get("produttore")
            fk_codice = req.form.get("codice")
            fk_codice_a_barre = req.form.get("codice_a_barre")
            fk_codice_art_fornitore = req.form.get("codice_articolo_fornitore")
            fk_id_famiglia_articolo = req.form.get("id_famiglia_articolo")
            fk_id_categoria_articolo = req.form.get("id_categoria_articolo")
            fk_id_stato_articolo = req.form.get("id_stato_articolo")
            fk_elminati = bool(req.form.get("eliminato"))
        elif req.args.get("searchkey"):
            dicio = eval(req.args.get("searchkey"))
            fk_denominazione = dicio["denominazione"]
            fk_produttore = dicio["produttore"]
            fk_codice = dicio["codice"]
            fk_codice_a_barre = dicio["codice_a_barre"]
            fk_codice_art_fornitore = dicio["codice_articolo_fornitore"]
            fk_id_famiglia_articolo = dicio["id_famiglia_articolo"]
            fk_id_categoria_articolo = dicio["id_categoria_articolo"]
            fk_id_stato_articolo = dicio["id_stato_articolo"]
            fk_elminati = bool(dicio["eliminato"])
        chiavi = { "denominazione" : fk_denominazione,
                    "produttore" : fk_produttore,
                    "codice" : fk_codice,
                    "codice_a_barre" : fk_codice_a_barre,
                    "codice_articolo_fornitore" : fk_codice_art_fornitore,
                    "id_famiglia_articolo": fk_id_famiglia_articolo,
                    "id_categoria_articolo" : fk_id_categoria_articolo,
                    "id_stato_articolo" : fk_id_stato_articolo,
                    "eliminato": fk_elminati}
        batch = 20
        count = Articolo(req=req).count(denominazione=fk_denominazione,
                                        produttore=fk_produttore,
                                        codice=fk_codice,
                                        codiceABarre = fk_codice_a_barre,
                                        codiceArticoloFornitore = fk_codice_art_fornitore,
                                        idFamiglia = fk_id_famiglia_articolo,
                                        idCategoria = fk_id_categoria_articolo,
                                        idStato = fk_id_stato_articolo,
                                        cancellato =fk_elminati)
        args = pagination(req,batch,count)
        args["page_list"] = "anagrafiche/articolo/list"
        daos = Articolo(req=req).select(denominazione=fk_denominazione,
                                        produttore=fk_produttore,
                                        codice=fk_codice,
                                        codiceABarre = fk_codice_a_barre,
                                        codiceArticoloFornitore = fk_codice_art_fornitore,
                                        idFamiglia = fk_id_famiglia_articolo,
                                        idCategoria = fk_id_categoria_articolo,
                                        idStato = fk_id_stato_articolo,
                                        cancellato =fk_elminati,
                                        batchSize=batch,
                                        offset=args["offset"])
        famiglie = FamigliaArticolo().select(batchSize=None)
        categorie = CategoriaArticolo().select(batchSize=None)
        statoarticolo = StatoArticolo().select(batchSize=None)
        pageData = {'file' : "anagraficaComplessa",
                    "_dao_":"articolo",
                    "name": "Articolo",
                    "tree":"treeArticolo",
                    "fkey":"fk_articolo",
                    "famiglie":famiglie,
                    "categorie": categorie,
                    "statoarticolo":statoarticolo,
                    "chiavi":chiavi,
                    "action":action,
                    "daos":daos,
                    "count":count,
                    "args":args}
        return Page(req).render(pageData)

    def __add__(req, action=None):
        """ TODO: Gestione dei campi obbligatori e delle chiavi duplicate"""
        id = req.form.get("id")
        if action == "add":
            dao = Articolo()
        else:
            dao = Articolo().getRecord(id=id)
        codice = req.form.get("codice")
        if codice:
            dao.codice = codice
        else:
            dao.codice = getNuovoCodiceArticolo()
        dao.denominazione = req.form.get("denominazione")
        dao.id_aliquota_iva = req.form.get("id_aliquota_iva")
        dao.id_famiglia_articolo = int(req.form.get("id_famiglia_articolo"))
        dao.id_categoria_articolo = int(req.form.get("id_categoria_articolo"))
        if req.form.get("id_stato_articolo"):
            dao.id_stato_articolo = int(req.form.get("id_stato_articolo"))
        if req.form.get("id_unita_base"):
            dao.id_unita_base = int(req.form.get("id_unita_base"))
        if req.form.get("id_imballaggio"):
            dao.id_imballaggio = int(req.form.get("id_imballaggio"))
        dao.lunghezza = float(req.form.get("lunghezza") or 0)
        dao.larghezza = float(req.form.get("larghezza") or 0)
        dao.altezza = float(req.form.get("altezza") or 0)
        dao.peso = float(req.form.get("peso") or 0)
        dao.peso_lordo = float(req.form.get("peso_lordo") or 0)
        dao.peso_imballaggio = float(req.form.get("peso_imballaggio")or 0)
        dao.quantita_minima = float(req.form.get("quantita_minima")or 0)
        dao.unita_dimensioni = req.form.get("unita_dimensioni")
        dao.produttore = req.form.get("produttore")
        dao.unita_volume = req.form.get("unita_volume")
        dao.volume = req.form.get("volume")
        dao.unita_peso = req.form.get("unita_peso")
        dao.codice_etichetta = req.form.get("codice_etichetta")
        dao.descrizione_etichetta = req.form.get("descrizione_etichetta")
        dao.descrizione_listino = req.form.get("descrizione_listino")
        dao.timestamp_variazione = datetime.datetime.now()
        dao.note = req.form.get("note")
        dao.contenuto = req.form.get("contenuto")
        dao.aggiornamento_listino_auto = bool(req.form.get("aggiornamento_listino_auto"))
        dao.stampa_etichetta = bool(req.form.get("stampa_etichetta"))
        dao.stampa_listino = bool(req.form.get("stampa_listino"))
        dao.sospeso = bool(req.form.get("sospeso"))
        dao.cancellato = False
        if codice \
                and req.form.get("denominazione") \
                and req.form.get("id_famiglia_articolo")\
                and req.form.get("id_categoria_articolo"):
            dao.persist()
        redirectUrl='/anagrafiche/articolo/list'
        return Page(req).redirect(redirectUrl)

    def __del__(req, action=None):
        """ TODO: Gestione delle chiavi non cancellabili """
        id = req.form.get("idr")
        dao = Articolo().getRecord(id=id)
        if dao:
            dao.delete()
        daos = Articolo(req=req).select(cancellato=True)
        pageData = {'file' : "/tree/treeArticolo",
                    "_dao_":"articolo",
                    "name": "Articolo",
                    "tree":"treeArticolo",
                    "action":action,
                    "daos":daos,
                    "count":len(daos)}
        return Page(req).render(pageData)

    def __edit__(req, action=None):
        id = req.form.get("idr")
        famiglie = FamigliaArticolo().select(batchSize=None)
        categorie = CategoriaArticolo().select(batchSize=None)
        aliquote = AliquotaIva().select(batchSize=None)
        imballaggi = Imballaggio().select(batchSize=None)
        unitabase = UnitaBase().select(batchSize=None)
        statoarticolo = StatoArticolo().select(batchSize=None)
        dao = Articolo().getRecord(id=id)
        pageData = {'file' : "/addedit/ae_articolo",
                    "_dao_":"articolo",
                    "famiglie":famiglie,
                    "categorie": categorie,
                    "aliquote":aliquote,
                    "imballaggi":imballaggi,
                    "unitabase":unitabase,
                    "statoarticolo":statoarticolo,
                    "name": "Articolo",
                    "tree":"treeArticolo",
                    "action":action,
                    "dao":dao}
        return Page(req).render(pageData)

    def __new__(req, action=None):
        famiglie = FamigliaArticolo().select(batchSize=None)
        categorie = CategoriaArticolo().select(batchSize=None)
        aliquote = AliquotaIva().select(batchSize=None)
        imballaggi = Imballaggio().select(batchSize=None)
        unitabase = UnitaBase().select(batchSize=None)
        statoarticolo = StatoArticolo().select(batchSize=None)
        pageData = {'file' : "/addedit/ae_articolo",
                    "_dao_":"articolo",
                    "famiglie":famiglie,
                    "categorie": categorie,
                    "aliquote":aliquote,
                    "imballaggi":imballaggi,
                    "unitabase":unitabase,
                    "statoarticolo":statoarticolo,
                    "name": "Articolo",
                    "tree":"treeArticolo",
                    "action":action,
                    }
        return Page(req).render(pageData)


    if action=="list":
        return _list_(req, action=action)
    elif action=="add" or action=="fromedit":
        return __add__(req, action=action)
    elif action=="delete":
        return __del__(req, action=action)
    elif action=="edit":
        return __edit__(req, action=action)
    elif action=="new":
        return __new__(req, action=action)


#  id serial NOT NULL,
#  codice character varying(50) NOT NULL,
#  denominazione character varying(300) NOT NULL,
#  id_aliquota_iva integer,
#  id_famiglia_articolo integer,
#  id_categoria_articolo integer,
#  id_immagine integer,
#  id_unita_base integer,
#  id_stato_articolo integer,
#  produttore character varying(150),
#  unita_dimensioni character varying(20),
#  lunghezza real,
#  larghezza real,
#  altezza real,
#  unita_volume character varying(20),
#  volume character varying(20),
#  unita_peso character varying(20),
#  peso_lordo real,
#  id_imballaggio integer,
#  peso_imballaggio real,
#  stampa_etichetta boolean,
#  codice_etichetta character varying(50),
#  descrizione_etichetta character varying(200),
#  stampa_listino boolean,
#  descrizione_listino character varying(200),
#  aggiornamento_listino_auto boolean,
#  timestamp_variazione timestamp without time zone,
#  note text,
#  contenuto text,
#  cancellato boolean,
#  sospeso boolean,
#  quantita_minima real,
