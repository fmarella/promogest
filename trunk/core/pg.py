#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
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
import sys
from optparse import OptionParser

class BigBang(object):
    def __init__(self, debug=None, shop=False):
        parser = OptionParser()
        debug_help = """Imposta una o piu' modalita' di debug tra
SQL, DAO, FILTER, ALL (separate da virgola)
per visualizzare rispettivamente le query SQL,
i DAO, i filtri o tutto"""
        parser.add_option("-d", "--debug",
                            action="store",
                            help=debug_help,
                            default="False",
                            type="string",
                            dest="debug")
        parser.add_option("-3", "--pg3",
                            action="store_true",
                            help="Utilizza il modulo gi e le librerie GTK+3",
                            default="False",
                            dest="pg3_classi")
        parser.add_option("-t", "--tipoDB",
                            action="store",
                            help="Imposta il backend DB (sqlite, postgresql)",
                            #default="False",
                            type="string",
                            dest="tipoDB")
        parser.add_option("-c", "--config-dir",
                            help="Specifica la cartella di configurazione",
                            #default="False",
                            type="string",
                            dest="configDir")
        parser.add_option("-f", "--config-file",
                            help="Specifica di configurazione",
                            #default="False",
                            type="string",
                            dest="configFile")
        parser.add_option("-r", "--rapid-start",
                            help="Imposta il tipo db e l'azienda (es. azienda@host)",
                            default="False",
                            type="string",
                            dest="RapidStart")
        parser.add_option("-n", "--nome_database",
                            help="Imposta il nome db",
                            #default="False",
                            type="string",
                            dest="nome_database")
        parser.add_option("-s", "--schema",
                            help="crea uno schema azienda",
                            #default="False",
                            type="string",
                            dest="schema")
        parser.add_option("-w", "--web",
                            help="simula un utulizzo web senza gtk",
                            action="store_true",
                            default="False",
                            dest="web")
        (options, args) = parser.parse_args()
        from promogest import preEnv, bindtextdomain
        bindtextdomain('promogest', locale_dir='./po/locale')
        reload(sys)
        sys.setdefaultencoding('utf-8')
        if options.configFile:
            from promogest.lib.config import Config
            conf = Config(options.configFile)
            preEnv.user = preEnv.userforce = conf.Database.user
            preEnv.database = preEnv.dbforce = conf.Database.database
            preEnv.password = preEnv.pwdforce= conf.Database.password
            preEnv.host = preEnv.hostdbforce = conf.Database.host
            preEnv.port = conf.Database.port
            preEnv.portforce = conf.Database.port
            preEnv.tipodb = preEnv.tipodbforce = conf.Database.tipodb
            preEnv.conf = conf

        if options.nome_database:
            preEnv.dbforce = options.nome_database
        if options.tipoDB:
            preEnv.tipodbforce = options.tipoDB
        if "@" in options.RapidStart:
            preEnv.aziendaforce = options.RapidStart.split("@")[0]
            preEnv.hostdbforce = options.RapidStart.split("@")[1]
        if 'ALL' in options.debug:
            preEnv.echo = True
        options.debug = options.debug.split(',')
        if 'DAO' in options.debug:
            preEnv.debugDao = True
        elif 'FILTER' in options.debug:
            preEnv.debugFilter = True
        if options.web == True:
            preEnv.web = True
        if options.tipoDB and options.schema:
            print(" DOBBIAMO CREARE UN NUOVO DB CON AZIENDA " ,  options.schema)
            preEnv.buildSchema = options.schema
            preEnv.aziendaforce = options.schema
            from createSchemaDb import buildAll
            buildAll()
            sys.exit()
        preEnv.table_to_load = ["promogest2.azienda", "promogest2.role" , "promogest2.action", "promogest2.roleaction","promogest2.utente"]
        from promogest.ui.Login import Login
        if shop:
            preEnv.shop = True
        login = Login()
        login.run()


if __name__ == '__main__':
    BigBang()
