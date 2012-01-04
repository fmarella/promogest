#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

from core.lib.utils import addSlash,includeFile
from core.lib.page import Page
#from core.dao.StaticPages import StaticPages

def homee(req, subdomain=None):
    """
    Home page
    """
    staticPages=None
    staticPages = StaticPages(req=req).select(permalink="la-tua-pubblicita-su-una-sola-riga")
    if staticPages:
        pag = "static"
        staticPages= staticPages[0]
    else:
        pag = "index"
    pageData = {'file' : pag,
                'subdomain': subdomain,
                'staticPages' : staticPages}
    return Page(req).render(pageData)
