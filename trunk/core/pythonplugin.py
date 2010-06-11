#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os

path = os.path.split(os.path.dirname(__file__))[0]
from promogest import Environment
Environment.conf.guiDir = path+"/core/gui/"
Environment.conf.decimals = 2
from promogest.ui.GladeWidget import *
from promogest.ui.widgets import PersonaGiuridicaSearchWidget, FornitoreSearchWidget,\
                    ClienteSearchWidget,ArticoloSearchWidget,CustomComboBoxModify,\
                    CustomComboBoxSearch,ScontiWidget,ScontoWidget
