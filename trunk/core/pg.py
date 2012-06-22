#!/usr/bin/env python
# -*- coding=utf-8 -*-
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

# coding=utf-8
import os
import sys
from optparse import OptionParser
#from promogest.lib.UpdateDB import *
from config import Config


class BigBang(object):
    def __init__(self, debug=None):
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
                            default="False",
                            type="string",
                            dest="tipoDB")
        parser.add_option("-c", "--config-dir",
                            help="Specifica la cartella di configurazione",
                            default="False",
                            type="string",
                            dest="configDir")
        parser.add_option("-r", "--rapid-start",
                            help="Imposta il tipo db e l'azienda (es. azienda@host)",
                            default="False",
                            type="string",
                            dest="RapidStart")
        parser.add_option("-n", "--nome_database",
                            help="Imposta il nome db",
                            default="False",
                            type="string",
                            dest="nome_database")
        (options, args) = parser.parse_args()
        from promogest import pg3_check, bindtextdomain
        bindtextdomain('promogest', locale_dir='./po/locale')
        if options.pg3_classi == True:
            reload(sys)
            sys.setdefaultencoding('utf-8')
            pg3_check.pg3_cla = True
        if options.nome_database:
            pg3_check.dbforce = options.nome_database
        if options.tipoDB:
            pg3_check.tipodbforce = options.tipoDB
        if "@" in options.RapidStart:
            pg3_check.aziendaforce = options.RapidStart.split("@")[0]
            pg3_check.hostdbforce = options.RapidStart.split("@")[1]
        if 'ALL' in options.debug:
            pg3_check.echo = True
        from promogest import Environment

        options.debug = options.debug.split(',')
        if 'DAO' in options.debug:
            Environment.debugDao = True
        elif 'FILTER' in options.debug:
            Environment.debugFilter = True
        elif 'SQL' in options.debug:
            Environment.debugSQL = True


        elif 'ALL' in options.debug:
            Environment.debugDao = True
            Environment.debugFilter = True
            Environment.debugSQL = True
        Environment.shop = False
        from promogest.ui.Login import Login
        login = Login()
        login.run()


if __name__ == '__main__':
    default = 'promogest2'
    #promogestStartDir = os.path.expanduser('~') + os.sep + default + os.sep
    #configFile = promogestStartDir + 'configure'
    #conf = Config(configFile)
    #try:
        #if conf.Database.tipodb =="sqlite":
            #import socket
            #import sys
            #import gtk
#            try:
#                s = socket.socket()
#                host = socket.gethostname()
#                port = 34639 #make sure this port is not used on this system
#                s.bind((host, port))
            #BigBang()
#            except Exception as e:
#                print "EEEEEEE", e
#                dialog = gtk.MessageDialog(None,
#                                           gtk.DIALOG_MODAL
#                                           | gtk.DIALOG_DESTROY_WITH_PARENT,
#                                           gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
#                                           "Un altro PromoGest ONE risulta già aperto\n\n")
#                response = dialog.run()
#                dialog.destroy()
#                raise
#                sys.exit()
        #else:
            #BigBang()
    #except:
        #BigBang()
    BigBang()
