# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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


from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.anagDocumenti.AnagraficaDocumentiFilter import \
                                                    AnagraficaDocumentiFilter
from promogest.ui.anagDocumenti.AnagraficaDocumentiEdit import \
                                                        AnagraficaDocumentiEdit
from promogest.dao.TestataDocumento import TestataDocumento
from promogest.lib.utils import *


class AnagraficaDocumenti(Anagrafica):
    """ Anagrafica documenti """

    def __init__(self, idMagazzino=None, aziendaStr=None):
        self._magazzinoFissato = (idMagazzino != None)
        self._idMagazzino = idMagazzino
        Anagrafica.__init__(self,
                        windowTitle=_('Promogest - Registrazione documenti'),
                        recordMenuLabel='_Documenti',
                        filterElement=AnagraficaDocumentiFilter(self),
                        htmlHandler=AnagraficaDocumentiHtml(self),
                        reportHandler=AnagraficaDocumentiReport(self),
                        editElement=AnagraficaDocumentiEdit(self),
                        aziendaStr=aziendaStr)
        self.records_file_export.set_sensitive(True)




    def aggiornaforniture(self):
        gl = setconf("General", "gestione_lotti")
        messageInfo(msg = "SI EFFETTUERA' ADESSO UN AGGIORNAMENTO PER I LOTTI\n ATTENDERE ANCHE QUALCHE MINUTO\n\n GRAZIE")
        if gl:
            #print " DEVI FARE LA CONVERSIONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", dir(self._anagrafica)
            #gobject.idle_add(self.pbar_anag_complessa.show)
            self.pbar_anag_complessa.show()
            from scripts.fixRigaMovForniture import fixRigaMovimentoTable
            fixRigaMovimentoTable(pbar_wid=self.pbar_anag_complessa)
            #gobject.idle_add(fixRigaMovimentoTable,self.pbar_anag_complessa)
        #else:
            #print "NON LA DEVI FAREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"


    def on_gestione_riba_menu_activate(self, widget):
        from promogest.ui.RiBaExportWindow import RiBaExportWindow
        anag = RiBaExportWindow(self)
        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(),
                                                None, self.filter.refresh)

    def duplicate(self, dao):
        """
        Duplica le informazioni relative ad un documento scelto su uno nuovo
        """
        if dao is None:
            return
        from promogest.ui.DuplicazioneDocumento import DuplicazioneDocumento
        anag = DuplicazioneDocumento(dao, self)
        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(),
                                                    None, self.filter.refresh)

    def on_record_fattura_button_clicked(self, button=None):
        from promogest.ui.FatturazioneDifferita import FatturazioneDifferita
        anag = FatturazioneDifferita(
                            self.anagrafica_filter_treeview.get_selection())
        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(),
                                button=None, callName=self.filter.refresh)


class AnagraficaDocumentiHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica, 'documento',
                                'Documento')

    def variations(self):
        aa= []
        if setconf("General", "gestione_lotti"):
            from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
            if self.dao:
                for r in self.dao.righe:
                    l = ""
                    #setattr(r, "aggiuntalottoindescrizione",l)
                    if self.dao.id_fornitore and r.id_articolo:
                        aa = RigaMovimentoFornitura().select(
                                    idRigaMovimentoAcquisto=r.id, batchSize=None)
                        #aa = r.rmfac
                    else:
                        aa = RigaMovimentoFornitura().select(
                                      idRigaMovimentoVendita=r.id, batchSize=None)
                        #aa = r.rmfve
                    #ll = r.descrizione
                    if aa:
                        lotti = []
                        scadenze = []
                        for a in aa:
                            lottostr = ""
                            scadstr = ""
                            if a.forni and a.forni.numero_lotto \
                                                and a.forni.numero_lotto != "":
                                lotto = a.forni.numero_lotto
                                if lotto in lotti:
                                    continue
                                else:
                                    lotti.append(lotto)
                                if lotto:
                                    lottostr = _("<br /> Lotto %s  - ") % lotto

                            if a.forni and a.forni.data_scadenza:
                                scad = dateToString(a.forni.data_scadenza)
                                if scad in scadenze:
                                    continue
                                else:
                                    scadenze.append(scad)
                                if scad:
                                    scadstr = _(" Data Sc. %s") % scad
                            l += lottostr + scadstr
                    else:
                        if setconf("Documenti", "lotto_temp"):
                            from promogest.dao.NumeroLottoTemp import NumeroLottoTemp
                            aa = NumeroLottoTemp().select(
                                            idRigaMovimentoVenditaTemp=r.id,
                                                batchSize=None)
                            #aa = r.NLT
                        if aa:
                            l += _("<br /> Lotto %s") % (aa[0].lotto_temp)
                    setattr(r, "aggiuntalottoindescrizione", l)
        return self.dao


class AnagraficaDocumentiReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description=_('Elenco dei documenti'),
                                  defaultFileName='documenti',
                                  htmlTemplate='documenti',
                                  sxwTemplate='documenti')
