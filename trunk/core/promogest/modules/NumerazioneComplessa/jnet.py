# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Francesco Meloni <francesco@promotux.it>

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

from promogest import Environment

#Commesse: 138.00-2010 (138 progressivo, .00- fisso, 2010 è l’anno)
#Ordini a magazzino: 002.00-MA2010 (sono uguali agli ordini ai fornitori ma ancora non sono oggetto di vendita, 002 progressivo, .00-MA fisso, 2010 è l’anno)
#Ordini beni strumentali: 029.00-BS2010 (sono gli ordini ai fornitori per materiali destinati ad uso ufficio, 029 progressivo, .00-BS fisso, 2010 l’anno)

#Offerte: 202JN2010 (202 progressivo, JN fisso, 2010 è l’anno)
#Ordini ai fornitori: 145.00-JN2010 (145 progressivo, .00-JN fisso, 2010 è l’anno)
#Documenti di trasporto: 084JN10-DDT (084 progressivo, JN fisso, 10 è l’anno, -DDT fisso)
#Fatture: F212JN2010 (F fisso, 212 progressivo, JN fisso, 2010 è l’anno)

def numerazioneJnet(dao):
    try:
        numero = dao.numero
    except:
        return
    if numero <10:
        new = "00"+str(numero)
    elif numero <100:
        new = "0"+str(numero)
    else:
        new = str(numero)

    if dao.operazione == "Fattura vendita":
        return "F"+str(new)+"JN"+str(Environment.workingYear)
    elif dao.operazione == "Fattura differita":
        return "F"+str(new)+"JN"+str(Environment.workingYear)
    elif "DDT" in dao.operazione:
        return str(new)+"JN"+str(Environment.workingYear)[2:]+"-DDT"
    elif dao.operazione == "Ordine a fornitore":
        return str(new)+".00-JN"+str(Environment.workingYear)
    elif dao.operazione == "Ordine a magazzino":
        return str(new)+".00-MA"+str(Environment.workingYear)
    elif dao.operazione == "Ordine beni strumentali":
        return str(new)+".00-BS"+str(Environment.workingYear)
    elif "Preventivo" in dao.operazione:
        return str(new)+"JN"+str(Environment.workingYear)
