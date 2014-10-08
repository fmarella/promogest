#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

import sys
import os
path = ".."
if path not in sys.path:
    sys.path.append(path)

#from promogest import preEnv

#preEnv.tipodbforce = "postgresql"
#preEnv.aziendaforce = "veterfarma"

#from promogest import Environment
import datetime
#from promogest.lib.utils import *
import serial


#from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino


#scons = TestataScontrino().select(batchSize=None, orderBy=desc("data_inserimento"))[:1]
#if scons:
    #daoScontrino = scons[0]

#print daoScontrino.righe
#from promogest.modules.VenditaDettaglio.lib.custom import Custom

#a = Custom()
#print "AAAAAAAAAAAAAAAAAAAAAAAAAAA", daoScontrino
#a.create_export_file(daoScontrino)


def serial_manager():
    ser = serial.Serial()
    ser.baud = 9600
    ser.port = '/dev/ttyUSB0'
    ser.xonxoff = True
    ser.open()
    print ser
    with open("scontrino_custom.txt","r") as f:
        scontr = f.read()
    #ser.write("1000H1R=15.25*2M100H4M1T")
    ser.write(scontr)
    f.close()
    ser.close()

serial_manager()
