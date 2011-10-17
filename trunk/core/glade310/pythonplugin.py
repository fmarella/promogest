#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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

import sys, os

path = os.path.split(os.path.dirname(__file__))[0]
core_path = os.path.join(os.path.split(os.path.abspath(path))[0], "core")
sys.path.append(core_path)
from promogest import pg3_check
pg3_check.pg3_cla = True
from promogest import Environment
Environment.conf.guiDir = path+"/gui/"
#Environment.conf.decimals = 2
from promogest.ui.GladeWidget import *
from promogest.ui.widgets import PersonaGiuridicaSearchWidget, FornitoreSearchWidget,\
                    ClienteSearchWidget,ArticoloSearchWidget,CustomComboBoxModify,\
                    CustomComboBoxSearch,ScontiWidget,ScontoWidget
