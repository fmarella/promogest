#!/usr/bin/env python
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


import os
from optparse import OptionParser
from promogest import Environment

class Shop(object):
    def __init__(self):
        usage = """Uso: %prog [options]
        Opzioni disponibili sono :
                -d   --debugDao Per visualizzare con delle print i dizionari dao
                """
        parser = OptionParser(usage=usage)
        parser.add_option("-d", "--debugDao",
                            action="store_true",
                            help="Per visualizzare con delle print i dizionari dao",
                            default="False",
                            #type="string",
                            dest="debugDao")


        (options, args) = parser.parse_args()

        from promogest import bindtextdomain
        bindtextdomain('promogest', locale_dir='./po/locale')

        from promogest.ui.Login import Login
        login = Login(shop=True)
        Environment.pg2log.info("APERTURA DI GESTIONE NEGOZIO")
        Environment.shop = True
        login.run()

if __name__ == '__main__':
    Shop()
