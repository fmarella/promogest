# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2009 by Promotux Informatica - http://www.promotux.it/

from promogest import Environment

MODULES_NAME = "Label"
MODULES_FOR_EXPORT = []
GUI_DIR = getattr(Environment.conf.Moduli, 'cartella_moduli', 'promogest/modules')+'/Label/gui/'
START_CALL_IS_IN_THREAD = True        # False if you  do NOT want to put execution
START_CALL = None                              # of this call in a separated Thread
TEMPLATES = getattr(Environment.conf.Moduli, 'cartella_moduli', 'promogest/modules')+'/Label/templates/'

#if Environment.conf.SuMisura.mod_enable == "yes":
    #if "SuMisura" not in Environment.modulesList:
        #Environment.modulesList.append("SuMisura")
