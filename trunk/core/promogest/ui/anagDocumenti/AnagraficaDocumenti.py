# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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


from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.anagDocumenti.AnagraficaDocumentiFilter import AnagraficaDocumentiFilter
from promogest.ui.anagDocumenti.AnagraficaDocumentiEdit import AnagraficaDocumentiEdit
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
        if Environment.azienda == "daog":
            from promogest.dao.Operazione import addOpDirette
            from promogest.dao.Setting import addregistriDiretti
            addOpDirette()
            addregistriDiretti()
        self.funzione_ordinamento = None
        self.aa = None


    def aggiornaforniture(self):
        gl = setconf("General", "gestione_lotti")
        if gl:
            from promogest.dao.Setconf import SetConf
            a = SetConf().select(key="fix_riga_movimento", section="General")
            if a and a[0].value =="False":
                messageInfo(msg = "SI EFFETTUERA' ADESSO UN AGGIORNAMENTO PER I LOTTI\n ATTENDERE ANCHE QUALCHE MINUTO\n\n GRAZIE")
                self.pbar_anag_complessa.show()
                from scripts.fixRigaMovForniture import fixRigaMovimentoTable
                fixRigaMovimentoTable(pbar_wid=self.pbar_anag_complessa)


    def on_gestione_riba_menu_activate(self, widget):
        if posso('GRB'):
            from promogest.modules.Riba.ui.RiBaExportWindow import RiBaExportWindow
            anag = RiBaExportWindow(self)
            showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(),
                                                    None, self.filter.refresh)
        else:
            fencemsg()

    def on_importa_ordine_json_activate(self, widget):
        #if posso('GRB'):
        from promogest.ui.ImportJsonDocumenti import ImportJsonDocumenti
        anag = ImportJsonDocumenti(self)
        showAnagraficaRichiamata(self.getTopLevel(), anag.getTopLevel(),
                                                None, self.filter.refresh)
        #else:
            #fencemsg()


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

    def on_segna_pagato_button_clicked(self, button=None):
        if YesNoDialog('Si sta chiudendo il pagamento per i documenti selezionati, continuare?'):
            selection = self.anagrafica_filter_treeview.get_selection()
            (model, iterator) = selection.get_selected_rows()
            for i in iterator:
                doc = model[i][0]
                doc.documento_saldato = True
                doc.totale_pagato = doc.totale_sospeso
                doc.totale_sospeso = 0
            Environment.session.commit()
            self.filter.refresh()


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
