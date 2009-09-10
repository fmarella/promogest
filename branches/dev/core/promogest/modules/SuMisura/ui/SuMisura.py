# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: JJDaNiMoTh <jjdanimoth@gmail.com>


from promogest import Environment

def CalcolaArea(altezza, larghezza):
    """
    Blabla
    """

    altezzamin = int(getattr(Environment.conf.SuMisura,'altezzamin'))
    larghezzamin = int(getattr(Environment.conf.SuMisura,'larghezzamin'))
    multiplo = int(getattr(Environment.conf.SuMisura,'errore_max'))

    if altezza < altezzamin:
        altezza = altezzamin
    if larghezza < larghezzamin:
        larghezza = larghezzamin

    restoH = altezza%multiplo
    restoL = larghezza%multiplo

    if restoH != 0:
        altezza = altezza + (multiplo - (restoH))
    if restoL != 0:
        larghezza = larghezza + (multiplo - (restoL))

    # Stiamo supponendo una quantita` in cm... nell'interfaccia c'e` scritto,
    # cm.. se sono un'unita` diversa, e` chiaro che questo codice non
    # funziona a dovere.

    metri_quadrati = (altezza * larghezza) * 0.0001
    metri_qqq = altezza * larghezza
    # ATTENZIONE inizialmente la funzione arrotondava a 4 cifre
    # si è momentaneamente portata a due ....vediamo 
    return ("%.2f" % metri_quadrati)

def CalcolaPerimetro(altezza, larghezza):
    """
    Blabla
    """
    metri_lineari = ((altezza + larghezza) * 2) * 0.01
    metri_qqq = (altezza + larghezza) *2
    return ("%.2f" % metri_lineari)
