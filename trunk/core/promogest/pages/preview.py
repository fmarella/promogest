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

def previews(req, views=None):
    """
    Funzione di gestione delle preview

    TODO: sostituire con una funzione di import definita non con exec

    """
    direct = "/preview/"
    idr = req.form.get("idr")
    daos = req.form.get("dao")
    exec "from promogest.dao."+daos+" import "+daos
    exec "dao=" +daos+"().getRecord(id="+idr+")"
    #files = direct+daos.lower()
    files = daos.lower()
    pageData = {'file' : files,
                "dao":dao}
    return Page(req).render(pageData)
