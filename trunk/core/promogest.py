#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Promogest
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# all rights reserved


import os
import sys

from optparse import OptionParser
from promogest import Environment
#from promogest.lib.UpdateDB import *
from config import Config

class BigBang(object):
    def __init__(self, debugDao=None, debugSQL=None, debugALL=None):
        usage = """Uso: %prog [options]
        Opzioni disponibili sono :
                -d   --debugDao Per visualizzare con delle print i dizionari dao
                -c   --config-dir Configurazione
                -f   --debugFilter Per visualizzare maggiori informazioni sui filtri
                -a   --debugALL Per mettere il debug al massimo
                -t   --tipoDB  Permette, quando possibile da modificare il DB
                        sottostante ( opzioni possibili: "sqlite" , "postgresql")
                """
        parser = OptionParser(usage=usage)
        parser.add_option("-d", "--debugDao",
                            action="store_true",
                            help="Per visualizzare con delle print i dizionari dao",
                            default="False",
                            #type="string",
                            dest="debugDao")
        parser.add_option("-a", "--debugALL",
                            action="store_true",
                            help="Per mettere il debug al massimo",
                            default="False",
                            #type="string",
                            dest="debugALL")
        parser.add_option("-t", "--tipoDB",
                            action="store",
                            help="Permette di cambiare backend DB da sqlite a postgresql",
                            default="False",
                            type="string",
                            dest="tipoDB")
        parser.add_option("-s", "--debugSQL",
                            action="store_true",
                            help="Per visualizzare con delle print l'echo di sqlalchemy",
                            default="False",
                            #type="string",
                            dest="debugSQL")
        parser.add_option("-f","--debugFilter",
                            help="Per visualizzare maggiori informazioni sui filtri",
                            action="store_true",
                            default="False",
                            dest="debugFilter")

        parser.add_option("-c","--config-dir",
                            help="Per visualizzare maggiori informazioni sui filtri",
                            default="False",
                            type="string",
                            dest="configDir")
        (options, args) = parser.parse_args()
        if options.debugDao == True:
            Environment.debugDao = True
        elif options.debugFilter == True:
            Environment.debugFilter = True
        elif options.debugSQL == True:
            Environment.debugSQL = True
        elif options.tipoDB == "sqlite":
            try:
                default='promogest2'
                promogestStartDir = os.path.expanduser('~') + os.sep + default + os.sep
                configFile = promogestStartDir + 'configure'
                conf = Config(configFile)
                oldDB = conf.Database.tipodb
                conf.Database.tipodb = "sqlite"
                conf.save()
                if oldDB != options.tipoDB:
                    print "ATTENZIONE !!!! RILANCIARE IL PROMOGEST A CAUSA DI UN CAMBIAMENTO DI DB"
                    return
            except:
                print "operazione non riuscita"
        elif options.tipoDB == "postgresql":
            try:
                default='promogest2'
                promogestStartDir = os.path.expanduser('~') + os.sep + default + os.sep
                configFile = promogestStartDir + 'configure'
                conf = Config(configFile)
                oldDB = conf.Database.tipodb
                conf.Database.tipodb = "postgresql"
                conf.save()
                if oldDB != options.tipoDB:
                    print "ATTENZIONE !!!! RILANCIARE IL PROMOGEST A CAUSA DI UN CAMBIAMENTO DI DB"
                    return
                #if options.datiConnessione""
            except:
                print "operazione non riuscita"
        elif options.debugALL == True:
            Environment.debugDao = True
            Environment.debugFilter = True
            Environment.debugSQL = True
        #print options.debugALL, options.debugSQL, debugDao
        Environment.shop = False
        from promogest.ui.Login import Login
        login = Login()
        login.run()


if __name__ == '__main__':
    default='promogest2'
    promogestStartDir = os.path.expanduser('~') + os.sep + default + os.sep
    configFile = promogestStartDir + 'configure'
    conf = Config(configFile)
    if conf.Database.tipodb =="sqlite":
        import socket
        import sys
        import gtk
        try:
            s = socket.socket()
            host = socket.gethostname()
            port = 35636    #make sure this port is not used on this system
            s.bind((host, port))
            BigBang()
        except Exception as e:
    #        raise
            dialog = gtk.MessageDialog(None,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                       "Un altro PromoGest ONE risulta già aperto\n\n")
            response = dialog.run()
            dialog.destroy()
            sys.exit()
    else:
        BigBang()
#    BigBang()
