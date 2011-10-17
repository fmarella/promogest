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
from promogest.dao.Azienda import Azienda
from datetime import datetime
from promogest import Environment

def siteAdminn(req, SUB =""):
    """
    classe di gestione dell"area riservata
    """
#    company = Azienda().select(batchSize=None)
    company = [Environment.azienda]
    anno = datetime.now().year
    pageData = {'file' : 'siteAdmin',
                "annocorrente":anno,
                'company': company}
    return Page(req).render(pageData)
