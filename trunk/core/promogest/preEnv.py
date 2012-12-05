# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@anche.no>

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



""" L'introduzione di questo file si è resa necessaria dal tentativo
di riordino di Environment, in questo file ci saranno dei parametri "force"
provenienti dagli argomenti di lancio diretti o indiretti come quelli
provenienti dal richiamo della app wsgi o web in genere, ci saranno però
anche i dati di connessione che passeranno ad EnvUtils ....per il momento
non trovo altra soluzione """

pg3_cla = False
shop = False
web = False
echo = False
debugFilter = False
debugDao = False
wsgi = False

aziendaforce = None
tipodbforce = None
hostdbforce = None
dbforce = None
userforce = None
portforce = None
pwdforce = None


pgwebconfpath = None

session = None
engine = None
conf = None
main_conf = None
main_conf_force = None

user = None
database = None
password = None
host = None
port = None
tipodb = None
azienda = None
SUB = ""

