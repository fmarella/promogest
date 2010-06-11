#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Promogest
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/
# all rights reserver


import os
#import sys

#from optparse import OptionParser
from promogest import Environment
#from promogest.lib.UpdateDB import *
#from config import Config

class ShopWin(object):
    def __init__(self):

        from Shop import Shop
        Shop = Shop()
        Environment.pg2log.info("APERTURA DI GESTIONE NEGOZIO")
        Environment.shop = True
        #login.run()

if __name__ == '__main__':
    ShopWin()
