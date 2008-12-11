#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# all rights reserver
# LICENSE: See LICENSE for more details.


from optparse import OptionParser
#from promogest.Environment import debugDao, debugSQL
from promogest.ui.Login import Login

class BigBang(object):
    def __init__(self, debugDao=None, debugSQL=None, debugALL=None):
        debugALL = None
        debugDao = None
        debugSQL = None
        usage = """Uso: %prog [options]
        Opzioni disponibili sono :
                --debugDao Per visualizzare con delle print i dao
                --debugSQL Per attivare l'echo di sqlalchemy
                --debugALL Per attivare entrambi i debug
                """
        parser = OptionParser(usage=usage)
        parser.add_option("-a", "--debugALL",
                            action="store_true",
                            help="Per attivare entrambi i debug",
                            default="False",
                            #type="string",
                            dest="debugALL")
        parser.add_option("-d", "--debugDao",
                            action="store_true",
                            help="Per visualizzare con delle print i dao",
                            default="False",
                            #type="string",
                            dest="debugDao")
        parser.add_option("-s", "--debugSQL",
                            action="store_true",
                            help="Per attivare l'echo di sqlalchemy",
                            #type="string",
                            default="False",
                            dest="debugSQL")
        #parser.add_option("-v","--verbose",
                            #help="rende l'operazione di creazione piu' dettagliata",
                            #action="store_true",
                            #dest="verbose")

        (options, args) = parser.parse_args()
        if options.debugDao == True:
            debugDao=options.debugDao
        elif options.debugSQL == True:
            debugSQL=options.debugSQL
        elif options.debugALL == True:
            debugDao=True
            debugSQL=True
        #print options.debugALL, options.debugSQL, debugDao
        login = Login(debugALL=debugALL, debugDao=debugDao, debugSQL= debugSQL )
        login.run()

if __name__ == '__main__':
    #login = Login()
    #login.run()
    BigBang()