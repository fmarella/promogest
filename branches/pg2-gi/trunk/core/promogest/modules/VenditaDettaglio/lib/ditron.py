# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005-2010 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francescoo@promotux.it>

from promogest import Environment
import datetime
#from datetime import *
from promogest.ui.utils import *
from  subprocess import *
import popen2


class Ditron(object):
    """
    Binding Python del driver ditron
    TODO: ripulire ed astrarre maggiormente
    """
    def __init__(self):
        pass

    def create_export_file(self, daoScontrino=None):
        # Genero nome file
        filename = Environment.conf.VenditaDettaglio.export_path\
                            + str(daoScontrino.id)\
                            + datetime.datetime.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename, 'w')

        # nel file scontrino i resi vengono vengono messi alla fine (limitazione cassa) DITRON
        righe = []
        for riga in daoScontrino.righe:
            if riga.quantita < 0:
                righe.append(riga)
            else:
                righe.insert(0, riga)

        for riga in righe:
            quantita = abs(riga.quantita)
            if quantita != 1:
                # quantita' non unitaria
                stringa = '000000000000000000%09d00\r\n' % (quantita * 1000)
                f.write(stringa)
            if riga.quantita < 0:
                # riga reso
                stringa = '020000000000000000%09d00\r\n' % (0)
                f.write(stringa)

            reparto = getattr(Environment.conf.VenditaDettaglio,
                                                    'reparto_default', 1)
            art = leggiArticolo(riga.id_articolo)
            repartoIva = 'reparto_' + art["denominazioneBreveAliquotaIva"].lower()
            if hasattr(Environment.conf.VenditaDettaglio, repartoIva):
                reparto = getattr(Environment.conf.VenditaDettaglio,
                                                        repartoIva, reparto)
            reparto = str(reparto).zfill(2)

            if not(riga.quantita < 0):
#                print "RIGA", riga.descrizione[:16], deaccenta(riga=riga.descrizione[:16])
                stringa = '01%-16s%09.2f%2s\r\n' % (deaccenta(riga=riga.descrizione[:16]), riga.prezzo, reparto)
                f.write(stringa)
                if riga.sconti:
                    for sconto in riga.sconti:
                        if sconto.valore != 0:
                            if sconto.tipo_sconto == 'percentuale':
                                stringa = '07%-16s%09.2f00\r\n' % ('sconto', sconto.valore)
                            else:
                                stringa = '06%-16s%09.2f00\r\n' % ('sconto', sconto.valore * quantita)

                            f.write(stringa)
            else:
#                print "RIGA", riga.descrizione[:16], deaccenta(riga=riga.descrizione[:16])
                # per i resi, nello scontrino, si scrive direttamente il prezzo scontato (limitazione cassa)
                stringa = '01%-16s%09.2f%2s\r\n' % (deaccenta(riga= riga.descrizione[:16]),
                                                riga.prezzo_scontato, reparto)
                f.write(stringa)

        if daoScontrino.totale_scontrino < daoScontrino.totale_subtotale and\
                                             daoScontrino.totale_sconto > 0:
            stringa='15                000000.0000\r\n'
            f.write(stringa)
            if daoScontrino.tipo_sconto_scontrino =='percentuale':
                stringa = '07%-16s%09.2f00\r\n' % ('sconto', daoScontrino.totale_sconto)
                f.write(stringa)
            else:
                stringa = '06%-16s%09.2f00\r\n' % ('sconto', daoScontrino.totale_sconto)
                f.write(stringa)

        if daoScontrino.totale_contanti is None or daoScontrino.totale_contanti == 0:
            totale_contanti = daoScontrino.totale_scontrino
        else:
            totale_contanti = daoScontrino.totale_contanti
        if daoScontrino.totale_assegni is not None and daoScontrino.totale_assegni != 0:
            stringa = '20                %09d00\r\n' % (daoScontrino.totale_assegni * 100)
            f.write(stringa)
        if daoScontrino.totale_carta_credito is not None and daoScontrino.totale_carta_credito != 0:
            stringa = '30                %09d00\r\n' % (daoScontrino.totale_carta_credito * 100)
            f.write(stringa)


        #stringa = '10                %09.2f00\r\n' % (totale_contanti)
        #f.write(stringa)
        stringa = '10                %09.2f00\r\n' % (totale_contanti)
        f.write(stringa)
        #stringa='71      Francesco Meloni     ..\r\n'
        #f.write(stringa)
        #stringa='71 CIAO A TUTTI              ..\r\n'
        #f.write(stringa)
        #stringa='71ARRIVEDERCI ALLA PROSSIMA  ..\r\n'
        #f.write(stringa)
        #stringa='72                00000000000..\r\n'
        #f.write(stringa)
        f.close()
        return filename

    def stampa_della_affluenza_oraria(self):
        filename = Environment.conf.VenditaDettaglio.export_path\
                     + 'stampa_della_affluenza_oraria_'\
                     + datetime.datetime.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename, 'w')
        stringa = '52                00000000009..\r\n'
        f.write(stringa)
        f.close()
        self.sendToPrint(filename)

    def stampa_del_periodico_articoli(self):
        filename = Environment.conf.VenditaDettaglio.export_path\
                     + 'stampa_del_periodico_articoli_'\
                     + datetime.datetime.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename, 'w')
        stringa = '52                00000000008..\r\n'
        f.write(stringa)
        f.close()
        self.sendToPrint(filename)

    def stampa_del_periodico_reparti(self):
        filename = Environment.conf.VenditaDettaglio.export_path\
                     + 'stampa_del_periodico_reparti_'\
                     + datetime.datetime.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename, 'w')
        stringa = '52                00000000006..\r\n'
        f.write(stringa)
        f.close()
        self.sendToPrint(filename)

    def stampa_del_periodico_cassa(self):
        filename = Environment.conf.VenditaDettaglio.export_path\
                     + 'stampa_del_periodico_cassa_'\
                     + datetime.datetime.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename, 'w')
        stringa = '52                00000000004..\r\n'
        f.write(stringa)
        f.close()
        self.sendToPrint(filename)

    def stampa_del_giornale_breve(self):
        filename = Environment.conf.VenditaDettaglio.export_path\
                    + 'stampa_del_giornale_breve_'\
                    + datetime.datetime.today().strftime('%d_%m_%Y_%H_%M_%S')
        f = file(filename, 'w')
        stringa = '52                00000000002..\r\n'
        f.write(stringa)
        f.close()
        self.sendToPrint(filename)

    def sendToPrint(self, filesToSend):
        """ Mando comando alle casse """
        program_launch = Environment.conf.VenditaDettaglio.driver_command
        program_params = (' ' + filesToSend + ' ' +
                            Environment.conf.VenditaDettaglio.serial_device)

        if os.name == 'nt':
            exportingProcessPid = os.spawnl(os.P_NOWAIT, program_launch, program_params)
            id, ret_value = os.waitpid(exportingProcessPid, 0)
            ret_value = ret_value >> 8
        else:
            command = program_launch + program_params
            process = popen2.Popen3(command, True)
            message = process.childerr.readlines()
            ret_value = process.wait()
        # Elimino il file
        os.remove(filesToSend)
        if ret_value != 0:
            string_message = ''
            for s in message:
                string_message = string_message + s + "\n"

            # Mostro messaggio di errore
            dialog = gtk.MessageDialog(None,
                                       gtk.DIALOG_MODAL
                                       | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                       string_message)
            response = dialog.run()
            dialog.destroy()
