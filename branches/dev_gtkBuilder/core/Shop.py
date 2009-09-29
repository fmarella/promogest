#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Promogest
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# all rights reserver


import os
#import sys

from optparse import OptionParser
from promogest import Environment
#from promogest.lib.UpdateDB import *
#from config import Config

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

        from promogest.ui.Login import Login
        login = Login(shop=True)
        Environment.pg2log.info("APERTURA DI GESTIONE NEGOZIO")
        Environment.shop = True
        login.run()

if __name__ == '__main__':
    Shop()
