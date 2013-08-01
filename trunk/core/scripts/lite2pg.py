#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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

"""
sqlite database .dump > /the/path/to/sqlite-dumpfile.sql

"""

promogest2 = ["action", "anno_abbigliamento", "applog"]
schema = "climax"
from promogest.Environment import params  , session , azienda
from promogest.lib.utils import stringToDateTime, setconf , timeit , pbar


@timeit
def lite2pg(pbar_wid=None):
    a = open("/home/vete/promogest2/sqlite-dumpfile.sql", "r")
    b = open("/home/vete/promogest2/sqlite-dumpfile_parsed.sql", "w")
    #print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", a.readline()
    for x in a.readlines()[0:3500]:
        #print x
        if "CREATE" in x:
            #print x
            tab = x.split(" ")[2]
            c = x.replace(tab, schema + "." + tab)
            b.write(c)
        elif "INSERT" in x:
            #print x
            tab = x.split(" ")[2]
            c = x.replace(tab, schema+"."+tab[1:-1])
            #print tab
            if tab == '"utente"':
                print c ,
                v = c[c.find("(")+1:c.find(")")].split(",")[7] = "TRUE"
                print " ANCORA ",v,c[c.find("(")+1:c.find(")")].split(","), c
                #c = c.replace(c[c.find("(")+1:c.find(")")].split(",")[7], "TRUE")
                #b.write(z)
                #c = c.replace(c[c.find("(")+1:c.find(")")].split(",")[11], "FALSE")
                #print "DEVO CAMBIARE IL BOOLEAN", x[x.find("(")+1:x.find(")")].split(",")[7] ,z
                #b.write(z)

            #if tab == '"articolo"':
                #print "DEVO CAMBIARE IL BOOLEAN" ,x.split("(")
            #if tab == '"account_emal"':
                #print "DEVO CAMBIARE IL BOOLEAN" ,x.split("(")
                print c
            b.write(c)

        elif "REFERENCES" in x:
            #print x
            befor_keyowrd, keyword, after_keyword = x.partition('REFERENCES')
            tab = after_keyword.split(" ")[1]
            c = after_keyword.replace(tab, schema + "." + tab)
            d = befor_keyowrd+keyword+c
            #print "DOPO",d
            b.write(d)
        elif "BLOB" in x:
            c = x.replace(x.split(" ")[1], "bytea")
            b.write(c)


        else:
            b.write(x)
    b.close()

if __name__ == '__main__':
    lite2pg()
