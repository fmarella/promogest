## -*- coding: utf-8 -*-
#import gobject
#import gtk

#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
#sys.stdout = sys.stderr
#path = '/home/mentore/pg2_work/branches/dev_gtkBuilder/core/'
#if path not in sys.path:
    #sys.path.append(path)

path = os.path.split(os.path.dirname(__file__))[0]
from promogest import Environment
Environment.conf.guiDir = path+"/core/gui/"
Environment.conf.decimals = 2
from promogest.ui.GladeWidget import *
from promogest.ui.widgets import PersonaGiuridicaSearchWidget, FornitoreSearchWidget,\
                    ClienteSearchWidget,ArticoloSearchWidget,CustomComboBoxModify,\
                    CustomComboBoxSearch,ScontiWidget,ScontoWidget

















