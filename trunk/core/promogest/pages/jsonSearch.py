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

from promogest.lib.page import Page
from promogest.lib.webutils import Response
from promogest.dao.Articolo import Articolo
from promogest.dao.Fornitura import Fornitura
from promogest.dao.Fornitore import Fornitore
import simplejson as json

def jsonsearch(req, action=None, what_json_search=None):
    """
    Funzione di gestione delle preview
    """
    fk = req.args.get("q")
    if what_json_search == "fk_json_articolo_denominazione":
        daos = Articolo().select(denominazione = fk)
        item = [{"value":d.id,"name":d.denominazione} for d in daos]
    elif what_json_search == "fk_json_articolo_produttore":
        daos = Articolo().select(produttore = fk)
        item = [{"value":d.id,"name":d.produttore} for d in daos]
    elif what_json_search == "fk_json_articolo_codice":
        daos = Articolo().select(codice = fk)
        item = [{"value":d.id,"name":d.codice} for d in daos]
    elif what_json_search == "fk_json_articolo_all":
        daos = Articolo().select(tutto = fk)
        item = [{"value":d.id,"name":d.codice} for d in daos]
    elif what_json_search == "fk_json_codice_articolo_fornitore":
        daos = Fornitura().select(codiceArticoloFornitore=fk)
        item = [{"value":d.id,"name":d.codice_articolo_fornitore} for d in daos]
    elif what_json_search == "fk_json_fornitore":
        daos = Fornitore().select(ragioneSociale=fk)
        item = [{"value":d.id,"name":d.ragione_sociale+d.cognome+" "+d.nome} for d in daos]
    jasoned = json.dumps(item)
    return Response(jasoned)
