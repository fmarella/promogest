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
from promogest.dao.Fornitura import Fornitura
from promogest.dao.Fornitore import Fornitore
from promogest.lib.webutils import *

def anagraficaFornitura(req, action=None):
    """
    Funzione di gestione delle preview
    """
    def _list_(req, action=None):
        """ """
        print "TO DICT", req.args.to_dict(), req.form.to_dict()
        fk_codice_articolo_fornitore = None
        fk_as_codice_articolo_fornitore = None
        fk_id_fornitore = None
        fk_id_articolo = None
        fk_da_data_prezzo = None
        fk_a_data_prezzo = None
        fk_da_data_fornitura = None
        fk_a_data_fornitura = None
        if req.form.to_dict():
            fk_codice_articolo_fornitore = req.form.get("codice_articolo_fornitore")
            if fk_codice_articolo_fornitore =="":
                fk_codice_articolo_fornitore = req.form.get("as_values_codice_articolo_fornitore").split(",")[0]
            fk_id_fornitore = req.form.get("id_fornitore")
            if fk_id_fornitore =="":
                fk_id_fornitore = req.form.get("as_values_id_fornitore").split(",")[0]
            fk_id_articolo = req.form.get("id_articolo")
            if fk_id_articolo =="":
                fk_id_articolo = req.form.get("as_values_id_articolo").split(",")[0]
            fk_da_data_prezzo = req.form.get("da_data_prezzo")
            fk_a_data_prezzo = req.form.get("a_data_prezzo")
            fk_da_data_fornitura = req.form.get("da_data_fornitura")
            fk_a_data_fornitura = req.form.get("a_data_fornitura")
        elif req.args.get("searchkey"):
            dicio = eval(req.args.get("searchkey"))
            print "DICIOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", dicio
            fk_codice_articolo_fornitore = dicio["codice_articolo_fornitore"]
            if fk_codice_articolo_fornitore =="":
                fk_codice_articolo_fornitore =dicio["as_values_codice_articolo_fornitore"]
            fk_id_fornitore = dicio["id_fornitore"]
            if fk_id_fornitore =="":

                fk_id_fornitore = dicio["as_values_id_fornitore"].split(",")[0]
            fk_id_articolo = dicio["id_articolo"]
            if fk_id_articolo =="":
                fk_id_articolo = dicio["as_values_id_articolo"].split(",")[0]
            fk_da_data_prezzo = dicio["da_data_prezzo"]
            fk_a_data_prezzo = dicio["a_data_prezzo"]
            fk_da_data_fornitura = dicio["da_data_fornitura"]
            fk_a_data_fornitura = dicio["a_data_fornitura"]
        chiavi = { "codice_articolo_fornitore" : fk_codice_articolo_fornitore,
                    "id_fornitore" : fk_id_fornitore,
                    "id_articolo" : fk_id_articolo,
                    "da_data_prezzo" : fk_da_data_prezzo,
                    "a_data_prezzo" : fk_a_data_prezzo,
                    "da_data_fornitura": fk_da_data_fornitura,
                    "a_data_fornitura" : fk_a_data_fornitura,}
        print "CHIAVIIIIIIIIIIIIIIIIIIIIIIIII", chiavi
        batch = 20
        count = Fornitura(req=req).count(codiceArticoloFornitore=fk_codice_articolo_fornitore,
                                        idFornitore=fk_id_fornitore,
                                        idArticolo=fk_id_articolo,
                                        daDataPrezzo = fk_da_data_prezzo,
                                        aDataPrezzo = fk_a_data_prezzo,
                                        daDataFornitura = fk_da_data_fornitura,
                                        aDataFornitura = fk_a_data_fornitura)
        args = pagination(req,batch,count)
        args["page_list"] = "anagrafiche/fornitura/list"
        daos = Fornitura(req=req).select(codiceArticoloFornitore=fk_codice_articolo_fornitore,
                                        idFornitore=fk_id_fornitore,
                                        idArticolo=fk_id_articolo,
                                        daDataPrezzo = fk_da_data_prezzo,
                                        aDataPrezzo = fk_a_data_prezzo,
                                        daDataFornitura = fk_da_data_fornitura,
                                        aDataFornitura = fk_a_data_fornitura,
                                        batchSize=batch,
                                        offset=args["offset"])

        pageData = {'file' : "anagraficaComplessa",
                    "_dao_":"fornitura",
                    "name": "Fornitura",
                    "tree":"treeFornitura",
                    "fkey":"fk_fornitura",
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
            dao = Fornitura()
        else:
            dao = Fornitura().getRecord(id=id)
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
        fornitori = Fornitore().select(batchSize=None)
        dao = Fornitura().getRecord(id=id)
        pageData = {'file' : "/addedit/ae_fornitura",
                    "_dao_":"fornitura",
                    "fornitori":fornitori,
                    "name": "Articolo",
                    "tree":"treeArticolo",
                    "action":action,
                    "dao":dao}
        return Page(req).render(pageData)

    def __new__(req, action=None):
        fornitori = Fornitore().select(batchSize=None)

        pageData = {'file' : "/addedit/ae_fornitura",
                    "_dao_":"fornitura",
                    "fornitori":fornitori,
                    "name": "Fornitura",
                    "tree":"treeFornitura",
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
