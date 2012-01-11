# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>

#    This file is part of Promogest. http://www.promogest.me

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

from promogest import Environment
from promogest.lib.page import Page
from promogest.dao.Promemoria import Promemoria
from promogest.dao.AnagraficaSecondaria import AnagraficaSecondaria_
from promogest.modules.RuoliAzioni.dao.Role import Role

def mainpage(req, subdomain=None):
    """
    Main
    """
    # PASSARE LE ATTIVITA' se azienda è giusto peso
    #prome = Promemoria().select(batchSize=None)
    #print "SUUUUUUUUUB2", subdomain, Environment.azienda
    role = Role().select(name="ATTIVITA")
    pgs = []
    if role:
        idrole = role[0].id
        pgs = AnagraficaSecondaria_().select(idRole=idrole, batchSize=None, orderBy="ragione_sociale")
        print "PEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", pgs
    pageData = {'file' : "mainpage",
                "pgs": pgs
                }
    return Page(req).render(pageData)
