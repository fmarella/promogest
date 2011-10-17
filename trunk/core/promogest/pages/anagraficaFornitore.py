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
from promogest.dao.Fornitore import Fornitore, getNuovoCodiceFornitore
from promogest.dao.PersonaGiuridica import PersonaGiuridica_ as PersonaGiuridica
from promogest.dao.Pagamento import Pagamento
from promogest.dao.Magazzino import Magazzino
from promogest.dao.CategoriaFornitore import CategoriaFornitore
from promogest.lib.webutils import *

def anagraficaFornitore(req, action=None):
    """
    Funzione di gestione delle preview
    """
    def _list_(req, action=None):
        """ """
        fk_ragione_sociale = None
        fk_insegna = None
        fk_cognome_e_nome = None
        fk_codice=None
        fk_localita = None
        fk_codice_fiscale = None
        fk_partita_iva = None
        fk_id_categoria_fornitore = None
        if req.form.to_dict():
            fk_ragione_sociale = req.form.get("ragione_sociale")
            fk_insegna = req.form.get("insegna")
            fk_cognome_e_nome = req.form.get("cognome_e_nome")
            fk_codice = req.form.get("codice")
            fk_localita = req.form.get("localita")
            fk_codice_fiscale = req.form.get("codice_fiscale")
            fk_partita_iva = req.form.get("partita_iva")
            fk_id_categoria_fornitore = req.form.get("id_categoria_fornitore")
        elif req.args.get("searchkey"):
            dicio = eval(req.args.get("searchkey"))
            fk_ragione_sociale = dicio["ragione_sociale"]
            fk_insegna = dicio["insegna"]
            fk_cognome_e_nome = dicio["cognome_e_nome"]
            fk_codice = dicio["codice"]
            fk_localita = dicio["localita"]
            fk_codice_fiscale = dicio["codice_fiscale"]
            fk_partita_iva = dicio["partita_iva"]
            fk_id_categoria_fornitore = dicio["id_categoria_fornitore"]
        chiavi = { "ragione_sociale" : fk_ragione_sociale,
                    "insegna" : fk_insegna,
                    "cognome_e_nome" : fk_cognome_e_nome,
                    "codice" : fk_codice,
                    "localita" : fk_localita,
                    "codice_fiscale": fk_codice_fiscale,
                    "partita_iva" : fk_partita_iva,
                    "id_categoria_fornitore" : fk_id_categoria_fornitore,
                        }
        batch = 20
        count = Fornitore(req=req).count(ragioneSociale=fk_ragione_sociale,
                                        insegna=fk_insegna,
                                        cognomeNome=fk_cognome_e_nome,
                                        codice = fk_codice,
                                        localita = fk_localita,
                                        codiceFiscale = fk_codice_fiscale,
                                        partitaIva = fk_partita_iva,
                                        idCategoria = fk_id_categoria_fornitore,
                                        )
        args = pagination(req,batch,count)
        args["page_list"] = "anagrafiche/fornitore/list"
        daos = Fornitore(req=req).select( ragioneSociale=fk_ragione_sociale,
                                        insegna=fk_insegna,
                                        cognomeNome=fk_cognome_e_nome,
                                        codice = fk_codice,
                                        localita = fk_localita,
                                        codiceFiscale = fk_codice_fiscale,
                                        partitaIva = fk_partita_iva,
                                        idCategoria = fk_id_categoria_fornitore,
                                        batchSize=batch,
                                        offset=args["offset"])
        categorie = CategoriaFornitore().select(batchSize=None)
        pageData = {'file' : "anagraficaComplessa",
                    "_dao_":"fornitore",
                    "name": "Fornitore",
                    "tree":"treeFornitore",
                    "fkey":"fk_fornitore",
                    "categorie":categorie,
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
            dao = Fornitore()
        else:
            dao = Fornitore().getRecord(id=id)
        codice = req.form.get("codice")
        if codice:
            dao.codice = codice
        else:
            dao.codice = getNuovoCodiceFornitore()
        if req.form.get("id_pagamento"):
            dao.id_pagamento = int(req.form.get("id_pagamento"))
        if req.form.get("id_magazzino"):
            dao.id_magazzino = int(req.form.get("id_magazzino"))
        # parte di tabella su persona giuridica
        dao.ragione_sociale = req.form.get("ragione_sociale")
        dao.insegna = req.form.get("insegna")
        dao.cognome = req.form.get("cognome")
        dao.nome = req.form.get("nome")
        dao.sede_operativa_indirizzo = req.form.get("sede_operativa_indirizzo")
        dao.sede_operativa_cap = req.form.get("sede_operativa_cap")
        dao.sede_operativa_provincia = req.form.get("sede_operativa_provincia")
        dao.sede_operativa_localita = req.form.get("sede_operativa_localita")
        dao.sede_legale_indirizzo = req.form.get("sede_legale_indirizzo")
        dao.sede_legale_cap = req.form.get("sede_legale_cap")
        dao.sede_legale_provincia = req.form.get("sede_legale_provincia")
        dao.sede_legale_localita = req.form.get("sede_legale_localita")
        #nazione    character varying(100)
        dao.codice_fiscale= req.form.get("codice_fiscale")
        dao.partita_iva = req.form.get("partita_iva")
        if dao.codice:
            dao.persist()
        redirectUrl='/anagrafiche/fornitore/list'
        return Page(req).redirect(redirectUrl)

    def __del__(req, action=None):
        """ TODO: Gestione delle chiavi non cancellabili """
        id = req.form.get("idr")
        dao = Fornitore().getRecord(id=id)
        if dao:
            dao.delete()
        daos = Fornitore(req=req).select()
        pageData = {'file' : "/tree/treeFornitore",
                    "_dao_":"fornitore",
                    "name": "Fornitore",
                    "tree":"treeFornitore",
                    "action":action,
                    "daos":daos}
        return Page(req).render(pageData)

    def __edit__(req, action=None):
        id = req.form.get("idr")
        pagamenti = Pagamento().select(batchSize=None)
        magazzini = Magazzino().select(batchSize=None)
        categoriefornitore = CategoriaFornitore().select(batchSize=None)
        dao = Fornitore().getRecord(id=id)
        idscateforn = [a.id_categoria_fornitore for a in dao.categoria]
        pageData = {'file' : "/addedit/ae_fornitore",
                    "_dao_":"fornitore",
                    "pagamenti":pagamenti,
                    "magazzini":magazzini,
                    "categoriefornitore":categoriefornitore,
                    "idscateforn":idscateforn,
                    "name": "Fornitore",
                    "tree":"treeFornitore",
                    "action":action,
                    "dao":dao}
        return Page(req).render(pageData)

    def __new__(req, action=None):
        pagamenti = Pagamento().select(batchSize=None)
        magazzini = Magazzino().select(batchSize=None)
        categoriefornitore = CategoriaFornitore().select(batchSize=None)
        pageData = {'file' : "/addedit/ae_fornitore",
                    "_dao_":"fornitore",
                    "name": "Fornitore",
                    "tree":"treeFornitore",
                    "action":action,
                    "pagamenti":pagamenti,
                    "magazzini":magazzini,
                    "categoriefornitore":categoriefornitore,
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
