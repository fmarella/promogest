# -*- coding: utf-8 -*-

#    Copyright (C) 2013 Francesco Marella <francesco.marella@anche.no>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#from promogest.ui.gtk_compat import *
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
from promogest.dao.TestataDocumento import TestataDocumento
from sqlalchemy import *
from datetime import datetime
from promogest.lib.utils import dateToString, stringToDateTime, mN, messageWarning, pbar


class ScadenzarioNotebookPage(GladeWidget):
    """ Informazioni sulle scadenze dei pagamenti."""

    da_pagare = True
    da_incassare = True
    in_scadenza = True
    scadute_non_pagate = False

    def __init__(self, maino, azienda):
        GladeWidget.__init__(self, root='scadenzario_frame',
                             path='scadenzario_notebook.glade')
        self.maino = maino
        self.aziendaStr = azienda or ""
        #self.on_aggiorna_button_clicked(None)

    def on_aggiorna_button_clicked(self, widget):
        # Alcuni controlli sull'input
        if self.periodo_checkbutton.get_active() and \
            (self.inizio_periodo_date.get_text() == '' or \
            self.fine_periodo_date.get_text() == ''):
                messageWarning('Inserire una data valida')
                return

        model = self.scadenzario_treeview.get_model()
        model.clear()

        if self.periodo_checkbutton.get_active():
            # Mostra le scadenze nel periodo
            tds = TestataDocumentoScadenza().select(orderBy=TestataDocumentoScadenza.data,
                    complexFilter=(and_(TestataDocumentoScadenza.data_pagamento==None,
                                        TestataDocumentoScadenza.data.between(stringToDateTime(self.inizio_periodo_date.get_text()),
                                                                              stringToDateTime(self.fine_periodo_date.get_text())))))
        else:
            # Mostra le prossime scadenze
            tds = TestataDocumentoScadenza().select(orderBy=TestataDocumentoScadenza.data,
                        complexFilter=(and_(TestataDocumentoScadenza.data_pagamento==None,
                                            TestataDocumentoScadenza.data>=datetime.now())))
        tipo_doc = ''
        for t in tds:
            doc = TestataDocumento().getRecord(id=t.id_testata_documento)
            if doc.operazione not in Environment.hapag:
                continue
            if doc.documento_saldato:
                continue
            if doc.id_fornitore and self.da_pagare:
                tipo_doc = 'A'
            if doc.id_cliente and self.da_incassare:
                tipo_doc = 'V'
            model.append([None, "%s" % dateToString(t.data),
                              "%s" % doc.intestatario,
                              tipo_doc,
                              "%s" % doc.numero, # numero documento
                              "€ %s" % mN(t.importo, 2), # importo
                              "", # descrizione
                              t.pagamento])

    def on_periodo_checkbutton_toggled(self, widget):
        if self.periodo_checkbutton.get_active():
            self.inizio_periodo_date.set_sensitive(True)
            self.fine_periodo_date.set_sensitive(True)
        else:
            self.inizio_periodo_date.set_sensitive(False)
            self.fine_periodo_date.set_sensitive(False)

    def on_da_pagare_checkbutton_toggled(self, widget):
        self.da_pagare = self.da_pagare_checkbutton.get_active()

    def on_da_incassare_checkbutton_toggled(self, widget):
        self.da_incassare = self.da_incassare_checkbutton.get_active()

    def on_in_scadenza_checkbutton_toggled(self, widget):
        self.in_scadenza = self.in_scadenza_checkbutton.get_active()

    def on_scadute_non_pagate_checkbutton_toggled(self, widget):
        self.scadute_non_pagate = self.scadute_non_pagate_checkbutton.get_active()
