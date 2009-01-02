# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/

from promogest import Environment

MODULES_NAME = "ImportPriceList"
MODULES_FOR_EXPORT = []
GUI_DIR = getattr(Environment.conf.Moduli, 'cartella_moduli', 'promogest/modules')+'/ImportPriceList/gui/'
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None                              # of this call in a separated Thread

#if Environment.conf.SuMisura.mod_enable == "yes":
    #if "SuMisura" not in Environment.modulesList:
        #Environment.modulesList.append("SuMisura")
