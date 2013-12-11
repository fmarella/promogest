# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

from promogest import Environment
#from promogest.buildEnv import set_configuration  #server per i test
import datetime
from promogest.lib.utils import *
from  subprocess import *
import popen2
import serial


class Custom(object):
    """
    Binding Python del driver custom
    “DESCRIZ. 1”1000H1R
    “DESCRIZ. 2”5*1000H1P
    =1000H4M
    “11393020158”@
    39F
    1T

    [VenditaDettaglio]
    backend = CUSTOM
    disabilita_stampa_chiusura = yes
    puntocassa = cassa01
    jolly = whatever
    migrazione_sincro_effettuata = si
    serial_device = /dev/ttyUSB0
    mod_enable = yes
    disabilita_stampa = no
    magazzino = whatever
    direct_confirm = yes
    export_path = /home/xxx/promogest2/xxx/temp/
    operazione = Scarico venduto da cassa
    primoavvio = no
    listino = whathever
    baud = 9600

    """
    def __init__(self):
        #conf = set_configuration(company=Environment.azienda) #serve per i test
        try: # vecchio stile ...adattamento ai dati in setconf
            #self.path = conf.VenditaDettaglio.export_path  #serve per i test
            self.path = Environment.VenditaDettaglio.export_path
        except: # prendo la cartella temp standard
            self.path = Environment.documentsDir
        # assegnazione_iva_reparti

    def create_export_file(self, daoScontrino=None):
        # Genero nome file
        filename = self.path\
                            + str(daoScontrino.id)\
                            + datetime.datetime.today().strftime('%d_%m_%Y_%H_%M_%S')+".txt"
        f = file(filename, 'w')
        righe = []
        #self.totali(daoScontrino)
        """Modificatori della vendita : Sconti e Maggiorazioni
Struttura della SINP:
<PR_VAL> <TERM> : per i modif. a valore
<QTY> <TERM> : per i modif. in %
Lista dei modificatori:
Funzione
Sconto % su transazione (item)           1
Sconto % su subtotale                    2
Sconto a valore su transazione (item)    3
Sconto a valore su subtotale             4
Magg. % su transazione (item)            5
Magg. % su subtotale                     6
Magg. a valore su transazione (item)     7
Magg. a valore su subtotale              8
Reso                                     9
Fondo cassa                             10
Prelievo di cassa                       11
Credito cliente                         12
"""

        for riga in daoScontrino.righe:
            #Forziamo la quantità come positiva
            quantita = abs(riga.quantita)
            sco = ""
            if riga.sconti:
                for sconto in riga.sconti:
                    if sconto.valore != 0:
                        if sconto.tipo_sconto == 'percentuale':
                            sco=str(sconto.valore)+"*1M"
                        else:
                            sco=str(sconto.valore * quantita)+"H3M\n"
            p = str(mN(riga.prezzo,2)).replace(".","")
            iva = riga.iva_articolo
            if iva and int(iva) == 22:
                rep = "1"
            elif iva and int(iva) == 10:
                rep = "2"
            elif iva and int(iva) == 4:
                rep = "3"
            elif iva and int(iva) == 0:
                rep = "4"
            if riga.quantita < 0:
                # riga reso
                stringa = '"'+ deaccenta(riga.descrizione[:19])+'"'+ str(quantita) +"*"+ p+'H9M'+"H"+rep+"R\n"
                f.write(stringa)
            elif quantita != 1:
                # quantita' non unitaria
                stringa = '"'+ deaccenta(riga.descrizione[:19])+'"'+ str(quantita) +"*"+ p+"H"+rep+"R"+sco+"\n"
                f.write(stringa)
            elif riga.quantita == 1:
                stringa = '"'+ deaccenta(riga.descrizione[:19])+'"'+ p+"H"+rep+"R"+sco+"\n"
                f.write(stringa)

            """ GESTIONE SUBTOTALE ED EVENTUALI SCONTI
Subtotale / Clear
Struttura della SINP:
7 di 15<TERM>
Es. Subtotale
<SINP>: [ = ]
Es. Vendita a reparto con sconto su subtotale e chiusura
<SINP>: [  ]
Es. Clear
<SINP>: [ K ]
Es. Annulla scontrino
<SINP>: [ k ]"""
        sco = ""
        if daoScontrino.sconti:

            for sconto in daoScontrino.sconti:
                if sconto.tipo_sconto =='percentuale':
                    sco += str(sconto.valore)+"*2M"
                else:
                    sco += str(sconto.valore)+"H4M"
        f.write("="+sco+"\n")

        """chiusure scontrino

        5.1.9. Chiusure di scontrino   [T]
Struttura della SINP:
<PR_VAL> <TERM>
Lista dei codici di chiusura (tender):

Funzione
Contanti          1
Assegni           2
Carte di credito  3
Buoni Pasto       4
Sospesi           5

Es. chiusura a contanti / assegni senza calcolo del resto:
9 di 15<SINP>: [ 1T ] / [ 2T ]
Es. chiusura a contanti / assegni con calcolo del resto:
<SINP>: [ 100000H1T ] / [ 20000H1T]"""

        t_scontrino = daoScontrino.totale_scontrino
        t_contanti = daoScontrino.totale_contanti
        t_assegni = daoScontrino.totale_assegni
        t_carta = daoScontrino.totale_carta_credito

        if t_contanti > 0 and t_assegni == 0 and t_carta == 0:
            #abbiamo un pagamento in contanti con gli altri metodi a zero
            f.write(str(mN(t_contanti,2)).replace(".", "") + "H1T\n")
        elif t_contanti == 0 and t_assegni > 0 and t_carta == 0:
            #abbiamo un pagamento con assegno con gli altri metodi a zero
            f.write(str(mN(t_contanti,2)).replace(".", "") + "H2T\n")
        elif t_contanti == 0 and t_assegni == 0 and t_carta > 0:
            #abbiamo un pagamento con carta con gli altri metodi a zero
            f.write(str(mN(t_contanti,2)).replace(".", "") + "H3T\n")
        elif t_contanti == 0 and t_assegni == 0 and t_carta == 0:
            #abbiamo un pagamento senza segnare contanti o altro
            f.write("1T\n")

        f.close()
        self.sendToPrint(filename)

    def sendToPrint(self, filesToSend):
        """ Mando comando alle casse """
        print "DEVO INVIARE IL FILE", filesToSend
        self.serial_manager(filesToSend)


    def serial_manager(self, filesToSend):
        ser = serial.Serial()
        try:
            Environment.conf.VenditaDettaglio.baud
        except:
            ser.baud = 9600
        #ser.port = '/dev/ttyUSB0'
        ser.port = Environment.conf.VenditaDettaglio.serial_device
        ser.xonxoff = True
        ser.open()
        #print ser
        with open(filesToSend,"r") as f:
            scontr = f.read()
        #ser.write("1000H1R=15.25*2M100H4M1T")
        #print scontr
        ser.write(scontr)
        f.close()
        ser.close()
