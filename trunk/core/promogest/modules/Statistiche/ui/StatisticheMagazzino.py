# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni  <francesco@promotux.it>

import os
import gtk
import time
import datetime
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.dao.TestataMovimento import TestataMovimento
from promogest.dao.RigaMovimento import RigaMovimento
from promogest.dao.Riga import Riga
from promogest.dao.Magazzino import Magazzino
from promogest.dao.Operazione import Operazione
from sqlalchemy import or_


class StatisticheMagazzino(GladeWidget):

    def __init__(self, idMagazzino=None):

        GladeWidget.__init__(self, 'statistiche_magazzino_dialog',
                'Statistiche/gui/statistiche_magazzino_elements.glade',
                isModule=True)
        self.placeWindow(self.getTopLevel())

        self._idMagazzino = idMagazzino
        self._orderingOrder = []
        self._groupingOrder = []

        self.giacenze_radiobutton.set_active(True)
        self.set_radiobutton_states()


    def on_window_close(self, widget, event):
        self.destroy()


    def set_radiobutton_states(self, button=None):
        self.active_giacenze_buttons(self.giacenze_radiobutton.get_active())
        self.active_venduti_buttons(self.venduto_radiobutton.get_active())


    def active_giacenze_buttons(self, val):
        self.ultimo_prezzo_acquisto_radiobutton.set_sensitive(val)
        self.ultimo_prezzo_vendita_radiobutton.set_sensitive(val)
        self.prezzo_medio_acquisto_radiobutton.set_sensitive(val)
        self.prezzo_medio_vendita_radiobutton.set_sensitive(val)
        self.ordinamento_famiglia_checkbutton.set_sensitive(val)
        self.ordinamento_categoria_checkbutton.set_sensitive(val)
        self.ordinamento_genere_checkbutton.set_sensitive(val)
        self.ordinamento_fornitore_checkbutton.set_sensitive(val)


    def active_venduti_buttons(self, val):
        self.da_data_entry.set_sensitive(val)
        self.a_data_entry.set_sensitive(val)
        self.raggruppamento_famiglia_checkbutton.set_sensitive(val)
        self.raggruppamento_categoria_checkbutton.set_sensitive(val)
        self.raggruppamento_genere_checkbutton.set_sensitive(val)
        self.raggruppamento_fornitore_checkbutton.set_sensitive(val)


    def on_any_checkbutton_giacenze_clicked(self, button):
        element = None
        if button == self.ordinamento_famiglia_checkbutton:
            element = 'famiglia'
        elif button == self.ordinamento_categoria_checkbutton:
            element = 'categoria'
        elif button == self.ordinamento_genere_checkbutton:
            element = 'genere'
        elif button == self.ordinamento_fornitore_checkbutton:
            element = 'fornitore'

        if element is None:
            return

        if button.get_active():
            self._orderingOrder.append(element)
        else:
            for s in range(len(self._orderingOrder)):
                if self._orderingOrder[s] == element:
                    self._orderingOrder.pop(s)
                    break


    def on_any_checkbutton_venduto_clicked(self, button):
        element = None
        if button == self.raggruppamento_famiglia_checkbutton:
            element = 'famiglia'
        elif button == self.raggruppamento_categoria_checkbutton:
            element = 'categoria'
        elif button == self.raggruppamento_genere_checkbutton:
            element = 'genere'
        elif button == self.raggruppamento_fornitore_checkbutton:
            element = 'fornitore'

        if element is None:
            return

        if button.get_active():
            self._groupingOrder.append(element)
        else:
            for s in range(len(self._groupingOrder)):
                if self._groupingOrder[s] == element:
                    self._groupingOrder.pop(s)
                    break


    def on_ok_button_clicked(self, button):
        fileDialog = gtk.FileChooserDialog(title='Salva la statistica ',
                                           parent=self.getTopLevel(),
                                           action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                           buttons=(gtk.STOCK_CANCEL,
                                                    gtk.RESPONSE_CANCEL,
                                                    gtk.STOCK_SAVE,
                                                    gtk.RESPONSE_OK),
                                           backend=None)


        folder = ''
        if hasattr(Environment.conf,'Documenti'):
            folder = getattr(Environment.conf.Documenti,'cartella_predefinita','')
        if folder == '':
            if os.name == 'posix':
                folder = os.environ['HOME']
            elif os.name == 'nt':
                folder = os.environ['USERPROFILE']
        fileDialog.set_current_folder(folder)

        fltr = gtk.FileFilter()
        fltr.add_mime_type('application/csv')
        fltr.set_name('File CSV (*.csv)')
        fileDialog.add_filter(fltr)

        fileDialog.set_current_name('stat_mag.csv')

        response = fileDialog.run()
        if response == gtk.RESPONSE_OK:
            filename = fileDialog.get_filename()
            fileDialog.destroy()

            self.export(filename)
        else:
            fileDialog.destroy()
            return


    def export(self, filename):
        intervallo = ''

        venduto = ('(SELECT R.id_articolo, ' +
            'SUM(R.quantita * R.moltiplicatore) AS quantita_ven, ' +
            'SUM(R.quantita * R.moltiplicatore * R.valore_unitario_netto) AS valore_ven ' +
            'FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id ' +
            'INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id ' +
            'INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione ' +
            'WHERE O.segno = \'-\' AND (O.tipo_persona_giuridica IS NULL OR O.tipo_persona_giuridica <> \'fornitore\') %s ' +
            'GROUP BY R.id_articolo) VV ON A.id = VV.id_articolo ')

        #venduto = Environment.params["session"]\
                #.query(RigaMovimento)\
                #.filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                #.filter(Operazione.denominazione == TestataMovimento.operazione)\
                #.filter(Operazione.segno =="-")\
                #.filter(or_(Operazione.tipo_persona_giuridica == None, Operazione.tipo_persona_giuridica !="fornitore"))\
                #.all()

        #print "venduto", venduto[0:10]

        acquistato = ('(SELECT R.id_articolo, ' +
                       'SUM(R.quantita * R.moltiplicatore) AS quantita_acq, ' +
                       'SUM(R.quantita * R.moltiplicatore * R.valore_unitario_netto) AS valore_acq ' +
                       'FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id ' +
                       'INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id ' +
                       'INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione ' +
                       'WHERE O.segno = \'+\' AND (O.tipo_persona_giuridica IS NULL OR O.tipo_persona_giuridica = \'fornitore\') %s ' +
                       'GROUP BY R.id_articolo) VA ON A.id = VA.id_articolo ')

        #acquistato = Environment.params["session"]\
                #.query(RigaMovimento)\
                #.filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                #.filter(Operazione.denominazione == TestataMovimento.operazione)\
                #.filter(Operazione.segno =="+")\
                #.filter(or_(Operazione.tipo_persona_giuridica == None, Operazione.tipo_persona_giuridica !="fornitore"))\
                #.all()

        #print "acquistato", acquistato[0:10]

        if self.giacenze_radiobutton.get_active():
            if self.ultimo_prezzo_acquisto_radiobutton.get_active():
                valorizzazione = ('LEFT OUTER JOIN (SELECT R.id_articolo, ' +
                                        'R.valore_unitario_netto AS prezzo, ' +
                                        'MAX(TM.data_movimento) ' +
                                        'FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id ' +
                                        'INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id ' +
                                        'INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione ' +
                                        'WHERE R.valore_unitario_netto <> 0 AND O.segno = \'+\' ' +
                                        'GROUP BY R.id_articolo, R.valore_unitario_netto) P ON A.id = P.id_articolo ')

            elif self.ultimo_prezzo_vendita_radiobutton.get_active():
                valorizzazione = ('LEFT OUTER JOIN (SELECT R.id_articolo, ' +
                                        'R.valore_unitario_netto AS prezzo, ' +
                                        'MAX(TM.data_movimento) ' +
                                        'FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id ' +
                                        'INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id ' +
                                        'INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione ' +
                                        'WHERE R.valore_unitario_netto <> 0 AND O.segno = \'-\' ' +
                                        'GROUP BY R.id_articolo, R.valore_unitario_netto) P ON A.id = P.id_articolo ')
            elif self.prezzo_medio_acquisto_radiobutton.get_active():
                valorizzazione = ('LEFT OUTER JOIN (SELECT R.id_articolo, ' +
                                        'AVG(R.valore_unitario_netto) AS prezzo, ' +
                                        'MAX(TM.data_movimento) ' +
                                        'FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id ' +
                                        'INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id ' +
                                        'INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione ' +
                                        'WHERE R.valore_unitario_netto <> 0 AND O.segno = \'+\' ' +
                                        'GROUP BY R.id_articolo) P ON A.id = P.id_articolo ')
            elif self.prezzo_medio_vendita_radiobutton.get_active():
                valorizzazione = ('LEFT OUTER JOIN (SELECT R.id_articolo, ' +
                                        'AVG(R.valore_unitario_netto) AS prezzo, ' +
                                        'MAX(TM.data_movimento) ' +
                                        'FROM riga_movimento RM INNER JOIN riga R ON RM.id = R.id ' +
                                        'INNER JOIN testata_movimento TM ON RM.id_testata_movimento = TM.id ' +
                                        'INNER JOIN promogest.operazione O ON TM.operazione = O.denominazione ' +
                                        'WHERE R.valore_unitario_netto <> 0 AND O.segno = \'-\' ' +
                                        'GROUP BY R.id_articolo) P ON A.id = P.id_articolo ')

            ordinamento = ''
            if len(self._orderingOrder) != 0:
                for o in self._orderingOrder:
                    if ordinamento != '':
                        ordinamento += ', '
                    if o == 'famiglia':
                        ordinamento += 'FA.denominazione'
                    elif o == 'categoria':
                        ordinamento += 'CA.denominazione'
                    elif o == 'genere':
                        ordinamento += 'GA.denominazione'
                    elif o == 'fornitore':
                        ordinamento += 'PG.ragione_sociale'
            if ordinamento != '':
                ordinamento += ', '
            ordinamento += 'A.codice'
            ordinamento = 'ORDER BY ' + ordinamento

            query = 'SET SEARCH_PATH TO ' + "rudolf" + ';\n\n'

            query += ('SELECT A.codice AS "Codice", ' +
                      'A.denominazione AS "Descrizione", ' +
                      'VA.quantita_acq as "Quantita\' acquistato", ' +
                      'G.quantita as "Quantita\'", ' +
                      'P.prezzo * G.quantita AS "Valore", ' +
                      'CB.codice AS "Codice a barre", ' +
                      'GT.denominazione AS "Gruppo taglia", ' +
                      'T.denominazione AS "Taglia", ' +
                      'C.denominazione AS "Colore", ' +
                      'AA.denominazione AS "Anno", ' +
                      'SA.denominazione AS "Stagione", ' +
                      'GA.denominazione AS "Genere", ' +
                      'FA.denominazione AS "Famiglia", ' +
                      'CA.denominazione AS "Categoria", ' +
                      'PG.codice AS "Codice fornitore", ' +
                      'PG.ragione_sociale AS "Fornitore" ' +
                      'FROM articolo A INNER JOIN ' +
                      '(SELECT id_articolo, SUM(giacenza) AS quantita FROM promogest.giacenzasel(\'' + "rudolf" + '\', 1, NULL, NULL, NULL) GROUP BY id_articolo) G ON A.id = G.id_articolo ' +
                      valorizzazione +
                      'LEFT OUTER JOIN' + (acquistato % '') +
                      'LEFT OUTER JOIN codice_a_barre_articolo CB ON CB.id_articolo = A.id AND CB.primario ' +
                      'LEFT OUTER JOIN articolo_taglia_colore ATC ON A.id = ATC.id_articolo ' +
                      'LEFT OUTER JOIN gruppo_taglia GT ON ATC.id_gruppo_taglia = GT.id ' +
                      'LEFT OUTER JOIN taglia T ON ATC.id_taglia = T.id ' +
                      'LEFT OUTER JOIN colore C ON ATC.id_colore = C.id ' +
                      'LEFT OUTER JOIN promogest.anno_abbigliamento AA ON ATC.id_anno = AA.id ' +
                      'LEFT OUTER JOIN promogest.stagione_abbigliamento SA ON ATC.id_stagione = SA.id ' +
                      'LEFT OUTER JOIN promogest.genere_abbigliamento GA ON ATC.id_genere = GA.id ' +
                      'LEFT OUTER JOIN famiglia_articolo FA ON A.id_famiglia_articolo = FA.id ' +
                      'LEFT OUTER JOIN categoria_articolo CA ON A.id_categoria_articolo = CA.id ' +
                      'LEFT OUTER JOIN fornitura FF ON FF.id_articolo = A.id ' +
                      'LEFT OUTER JOIN fornitore FO ON FF.id_fornitore = FO.id ' +
                      'LEFT OUTER JOIN persona_giuridica PG ON FO.id = PG.id ' +
                      ordinamento +
                      ';\n')
            print "PRIMA QUERYYYYYYYYYYYYYYYYY", query

            argList = []

            Environment.connection._cursor.execute(query, argList)
            res = Environment.connection._cursor.fetchall()

            f = open(filename,'w')
            riga = ('Codice, Descrizione, Quantita\' acquistata, Quantita\', Valore, Codice a barre, ' +
                    'Gruppo taglia, Taglia, Colore, Anno, Stagione, Genere, ' +
                    'Famiglia, Categoria, Codice fornitore, Fornitore\n')
            f.write(riga)
            for r in res:
                quantita_acquistata = '%14.4f' % float(r["Quantita\' acquistato"] or 0)
                quantita_acquistata = quantita_acquistata.replace('.',',')
                quantita = '%14.4f' % float(r["Quantita\'"] or 0)
                quantita = quantita.replace('.',',')
                valore = '%14.4f' % float(r["Valore"] or 0)
                valore = valore.replace('.',',')
                riga = ('"' + str(r["Codice"] or '') + '",' +
                        '"' + str(r["Descrizione"] or '') + '",' +
                        '"' + quantita_acquistata + '",' +
                        '"' + quantita + '",' +
                        '"' + valore + '",' +
                        '"' + str(r["Codice a barre"] or '') + '",' +
                        '"' + str(r["Gruppo taglia"] or '') + '",' +
                        '"' + str(r["Taglia"] or '') + '",' +
                        '"' + str(r["Colore"] or '') + '",' +
                        '"' + str(r["Anno"] or '') + '",' +
                        '"' + str(r["Stagione"] or '') + '",' +
                        '"' + str(r["Genere"] or '') + '",' +
                        '"' + str(r["Famiglia"] or '') + '",' +
                        '"' + str(r["Categoria"] or '') + '",' +
                        '"' + str(r["Codice fornitore"] or '') + '",' +
                        '"' + str(r["Fornitore"] or '') + '"\n')
                f.write(riga)
            f.close()
        elif self.venduto_radiobutton.get_active():
            intervallo = ''
            if self.da_data_entry.get_text() != '':
                d = time.strptime(self.da_data_entry.get_text(), "%d/%m/%Y")
                data = str(d[0]) + '-' + str(d[1]) + '-' + str(d[2])
                intervallo += 'AND TM.data_movimento >= \'' + data + '\' '
            if self.a_data_entry.get_text() != '':
                d = time.strptime(self.a_data_entry.get_text(), "%d/%m/%Y")
                data = str(d[0]) + '-' + str(d[1]) + '-' + str(d[2])
                intervallo += 'AND TM.data_movimento <= \'' + data + '\' '

            query = 'SET SEARCH_PATH TO ' + Environment.connection._schemaAzienda + ';\n\n'

            if len(self._groupingOrder) == 0:
                query += ('SELECT A.codice AS "Codice", ' +
                          'A.denominazione AS "Descrizione", ' +
                          'VA.quantita_acq as "Quantita\' acquistato", ' +
                          'VV.quantita_ven as "Quantita\' venduto", ' +
                          'VV.valore_ven as "Valore venduto", ' +
                          'CB.codice AS "Codice a barre", ' +
                          'GT.denominazione AS "Gruppo taglia", ' +
                          'T.denominazione AS "Taglia", ' +
                          'C.denominazione AS "Colore", ' +
                          'AA.denominazione AS "Anno", ' +
                          'SA.denominazione AS "Stagione", ' +
                          'GA.denominazione AS "Genere", ' +
                          'FA.denominazione AS "Famiglia", ' +
                          'CA.denominazione AS "Categoria", ' +
                          'PG.codice AS "Codice fornitore", ' +
                          'PG.ragione_sociale AS "Fornitore" ' +
                          'FROM articolo A ' +
                          'LEFT OUTER JOIN' + (venduto % intervallo) +
                          'LEFT OUTER JOIN' + (acquistato % intervallo) +
                          'LEFT OUTER JOIN codice_a_barre_articolo CB ON CB.id_articolo = A.id AND CB.primario ' +
                          'LEFT OUTER JOIN articolo_taglia_colore ATC ON A.id = ATC.id_articolo ' +
                          'LEFT OUTER JOIN gruppo_taglia GT ON ATC.id_gruppo_taglia = GT.id ' +
                          'LEFT OUTER JOIN taglia T ON ATC.id_taglia = T.id ' +
                          'LEFT OUTER JOIN colore C ON ATC.id_colore = C.id ' +
                          'LEFT OUTER JOIN promogest.anno_abbigliamento AA ON ATC.id_anno = AA.id ' +
                          'LEFT OUTER JOIN promogest.stagione_abbigliamento SA ON ATC.id_stagione = SA.id ' +
                          'LEFT OUTER JOIN promogest.genere_abbigliamento GA ON ATC.id_genere = GA.id ' +
                          'LEFT OUTER JOIN famiglia_articolo FA ON A.id_famiglia_articolo = FA.id ' +
                          'LEFT OUTER JOIN categoria_articolo CA ON A.id_categoria_articolo = CA.id ' +
                          'LEFT OUTER JOIN fornitura FF ON FF.id_articolo = A.id ' +
                          'LEFT OUTER JOIN fornitore FO ON FF.id_fornitore = FO.id ' +
                          'LEFT OUTER JOIN persona_giuridica PG ON FO.id = PG.id ' +
                          'ORDER BY A.codice;\n')

                #print query

                argList = []
                Environment.connection._cursor.execute(query, argList)
                res = Environment.connection._cursor.fetchall()

                f = open(filename,'w')
                riga = ('Codice, Descrizione, Quantita\' acquistato, Quantita\' venduto, Valore venduto, Codice a barre, ' +
                        'Gruppo taglia, Taglia, Colore, Anno, Stagione, Genere, ' +
                        'Famiglia, Categoria, Codice fornitore, Fornitore\n')
                f.write(riga)
                for r in res:
                    quantita_acquistata = '%14.4f' % float(r["Quantita\' acquistato"] or 0)
                    quantita_acquistata = quantita_acquistata.replace('.',',')
                    quantita = '%14.4f' % float(r["Quantita\' venduto"] or 0)
                    quantita = quantita.replace('.',',')
                    valore = '%14.4f' % float(r["Valore venduto"] or 0)
                    valore = valore.replace('.',',')
                    riga = ('"' + str(r["Codice"] or '') + '",' +
                            '"' + str(r["Descrizione"] or '') + '",' +
                            '"' + quantita_acquistata + '",' +
                            '"' + quantita + '",' +
                            '"' + valore + '",' +
                            '"' + str(r["Codice a barre"] or '') + '",' +
                            '"' + str(r["Gruppo taglia"] or '') + '",' +
                            '"' + str(r["Taglia"] or '') + '",' +
                            '"' + str(r["Colore"] or '') + '",' +
                            '"' + str(r["Anno"] or '') + '",' +
                            '"' + str(r["Stagione"] or '') + '",' +
                            '"' + str(r["Genere"] or '') + '",' +
                            '"' + str(r["Famiglia"] or '') + '",' +
                            '"' + str(r["Categoria"] or '') + '",' +
                            '"' + str(r["Codice fornitore"] or '') + '",' +
                            '"' + str(r["Fornitore"] or '') + '"\n')
                    f.write(riga)
                f.close()
            else:
                clausola = ''
                for o in self._groupingOrder:
                    if clausola != '':
                        clausola += ', '
                    if o == 'famiglia':
                        clausola += 'FA.denominazione'
                    elif o == 'categoria':
                        clausola += 'CA.denominazione'
                    elif o == 'genere':
                        clausola += 'GA.denominazione'
                    elif o == 'fornitore':
                        clausola += 'PG.ragione_sociale'
                raggruppamento = 'GROUP BY ' + clausola
                ordinamento = 'ORDER BY ' + clausola

                query += ('SELECT SUM(VA.quantita_acq) as "Quantita\' acquistato", ' +
                          'SUM(VV.quantita_ven) as "Quantita\' venduto", ' +
                          'SUM(VV.valore_ven) as "Valore venduto" ')
                if 'genere' in self._groupingOrder:
                    query += ', GA.denominazione AS "Genere"'
                if 'famiglia' in self._groupingOrder:
                    query += ', FA.denominazione AS "Famiglia"'
                if 'categoria' in self._groupingOrder:
                    query += ', CA.denominazione AS "Categoria"'
                if 'fornitore' in self._groupingOrder:
                    query += ', PG.ragione_sociale AS "Fornitore"'
                query += (' FROM articolo A ' +
                          'LEFT OUTER JOIN ' + (venduto % intervallo) +
                          'LEFT OUTER JOIN ' + (acquistato % intervallo) +
                          'LEFT OUTER JOIN articolo_taglia_colore ATC ON A.id = ATC.id_articolo ')
                if 'genere' in self._groupingOrder:
                    query += 'LEFT OUTER JOIN promogest.genere_abbigliamento GA ON ATC.id_genere = GA.id '
                if 'famiglia' in self._groupingOrder:
                    query += 'LEFT OUTER JOIN famiglia_articolo FA ON A.id_famiglia_articolo = FA.id '
                if 'categoria' in self._groupingOrder:
                    query += 'LEFT OUTER JOIN categoria_articolo CA ON A.id_categoria_articolo = CA.id '
                if 'fornitore' in self._groupingOrder:
                    query += ('LEFT OUTER JOIN fornitura FF ON FF.id_articolo = A.id ' +
                              'LEFT OUTER JOIN fornitore FO ON FF.id_fornitore = FO.id ' +
                              'LEFT OUTER JOIN persona_giuridica PG ON FO.id = PG.id ')
                query += raggruppamento
                query += ' ' + ordinamento
                query += ';\n'

                #print query

                argList = []
                Environment.connection._cursor.execute(query, argList)
                res = Environment.connection._cursor.fetchall()

                f = open(filename,'w')
                riga = 'Quantita\' acquistato, Quantita\' venduto, Valore venduto, '
                if 'genere' in self._groupingOrder:
                    riga += 'Genere, '
                if 'famiglia' in self._groupingOrder:
                    riga += 'Famiglia, '
                if 'categoria' in self._groupingOrder:
                    riga += 'Categoria, '
                if 'fornitore' in self._groupingOrder:
                    riga += 'Fornitore, '
                riga += '\n'
                f.write(riga)
                for r in res:
                    quantita_acquistata = '%14.4f' % float(r["Quantita\' acquistato"] or 0)
                    quantita_acquistata = quantita_acquistata.replace('.',',')
                    quantita = '%14.4f' % float(r["Quantita\' venduto"] or 0)
                    quantita = quantita.replace('.',',')
                    valore = '%14.4f' % float(r["Valore venduto"] or 0)
                    valore = valore.replace('.',',')
                    riga = ('"' + quantita_acquistata + '",' +
                            '"' + quantita + '",' +
                            '"' + valore + '"')
                    if 'genere' in self._groupingOrder:
                        riga += ',"' + str(r["Genere"] or '') + '"'
                    if 'famiglia' in self._groupingOrder:
                        riga += ',"' + str(r["Famiglia"] or '') + '"'
                    if 'categoria' in self._groupingOrder:
                        riga += ',"' + str(r["Categoria"] or '') + '"'
                    if 'fornitore' in self._groupingOrder:
                        riga += ',"' + str(r["Fornitore"] or '') + '"'
                    riga += '\n'
                    f.write(riga)
                f.close()


        dialog = gtk.MessageDialog(self.getTopLevel(), gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_OK, '\n\nEsportazione terminata !')
        dialog.run()
        dialog.destroy()

