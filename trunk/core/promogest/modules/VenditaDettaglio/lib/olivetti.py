# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

import os
import datetime
from promogest import Environment
from promogest.ui.utils import *
import shutil

class ElaExecute(object):
    """
    Binding Python del driver elaExecute delle casse Olivetti prt100
    TODO: ripulire ed astrarre maggiormente
    Modelli supportati:
    # Nettuna 200
    # Nettuna 400
    # Nettuna 500
    # Nettuna 600
    # Nettuna JET
    # PRT100F
    # PRT100FX
    """
    def __init__(self):
        pass
#1325 ; 30,43 ; TRANCIO MORTADELLA DOLCE ; 1 ; 5,646 x 5,39
    def create_export_file(self, daoScontrino=None):
        # Genero nome file
        filename = Environment.tempDir\
                            + str(daoScontrino.id)\
                            + datetime.datetime.today().strftime('%d_%m_%Y_%H_%M_%S')+".txt"
        f = file(filename, 'w')
        #print "DAO SCRONRTINOOOOOOOOOOOOO2", daoScontrino , daoScontrino.__dict__
        # nel file scontrino i resi vengono vengono messi alla fine (limitazione cassa) DITRON
        righe = []
#        for riga in daoScontrino.righe:
#            if riga.quantita < 0:
#                righe.append(riga)
#            else:
#                righe.insert(0, riga)
        f.write("1322\n")
        for riga in daoScontrino.righe:
            quantita = abs(riga.quantita)
            if riga.quantita < 0:
                # riga reso
                stringa = '020000000000000000%09d00\r\n' % (0)
                f.write(stringa)
            elif quantita != 1:
                # quantita' non unitaria
                stringa = "1325;"+str(quantita*riga.prezzo)+" ; "+deaccenta(riga.descrizione[:16])+" ; ; "+ str(quantita) +"x"+ str(riga.prezzo)+"\n"
                f.write(stringa)


#            reparto = getattr(Environment.conf.VenditaDettaglio,
#                                                    'reparto_default', 1)
#            art = leggiArticolo(riga.id_articolo)
#            repartoIva = 'reparto_' + art["denominazioneBreveAliquotaIva"].lower()
#            if hasattr(Environment.conf.VenditaDettaglio, repartoIva):
#                reparto = getattr(Environment.conf.VenditaDettaglio,
#                                                        repartoIva, reparto)
#            reparto = str(reparto).zfill(2)

            elif not (riga.quantita < 0):
                stringa = "1325 ; "+str(riga.prezzo).replace(".",",")+" ; "+deaccenta(riga.descrizione[:16])+"\n"
                f.write(stringa)
                if riga.sconti:
                    for sconto in riga.sconti:
                        if sconto.valore != 0:
                            if sconto.tipo_sconto == 'percentuale':
                                stringa="1327 ; "+str(riga.prezzo-riga.prezzo_scontato) +" ; %s%%\n" %str(sconto.valore).replace(".",",")
                            else:
                                stringa="1327 ; "+ str(sconto.valore * quantita)+" ; %s euro\n" % (str(sconto.valore * quantita).replace(".",","))
                            f.write(stringa)
            else:
                # per i resi, nello scontrino, si scrive direttamente il prezzo scontato (limitazione cassa)
                stringa = '01%-16s%09.2f%2s\r\n' % (self.deaccenta(riga.descrizione[:16]),
                                                riga.prezzo_scontato, reparto)
                f.write(stringa)

        if daoScontrino.totale_scontrino < daoScontrino.totale_subtotale and\
                                             daoScontrino.totale_sconto > 0:
            if daoScontrino.tipo_sconto_scontrino =='percentuale':
                stringa="1327 ; "+str(daoScontrino.totale_subtotale-daoScontrino.totale_scontrino) +" ; %s%%\n" %str(daoScontrino.totale_sconto).replace(".",",")
                f.write(stringa)
            else:
                stringa="1327 ; "+ str(daoScontrino.totale_sconto)+";%s euro\n" %str(daoScontrino.totale_sconto)
                f.write(stringa)
        if daoScontrino.totale_contanti == 0 and daoScontrino.totale_assegni == 0 and daoScontrino.totale_carta_credito == 0:
            totale_contanti = daoScontrino.totale_scontrino
            f.write("1329 ; "+str(totale_contanti).replace(".",",")+";Contanti\n")
        elif daoScontrino.totale_contanti and daoScontrino.totale_assegni == 0 and daoScontrino.totale_carta_credito == 0:
            totale_contanti = daoScontrino.totale_contanti
            f.write("1329 ; "+str(totale_contanti).replace(".",",")+";Contanti\n")
        elif daoScontrino.totale_contanti == 0 and daoScontrino.totale_assegni != 0 and daoScontrino.totale_carta_credito == 0:
            f.write("1329 ; ; Assegno\n")
        elif daoScontrino.totale_contanti == 0 and daoScontrino.totale_carta_credito != 0 and daoScontrino.totale_assegni == 0:
            f.write("1329 ; ; Carta/Bancomat\n")
        else:
            print "SITUAZIONE POCO CHIARA METTO UN VALORE SEMPLICE "
            f.write("1329\n")

        f.write("1323\n")
        f.write("912 ; 1\n")
        f.close()
        self.copyToInDir(filename)

        return filename

    def copyToInDir(self, filename):
        #shutil.copy(filename, "/opt/ela_execute/in/")
        if hasattr(Environment.conf, "VenditaDettaglio"):
            if hasattr(Environment.conf.VenditaDettaglio,"export_path"):
                path = Environment.conf.VenditaDettaglio.export_path
                #print "filename 111111111111111111111111111111", filename, path
                if not os.path.exists(filename):
                    shutil.move(filename, path)
