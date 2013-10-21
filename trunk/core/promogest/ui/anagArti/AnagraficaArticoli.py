# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
#    Author: Francesco Marella  <francesco.marella@anche.no>

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

from promogest.ui.gtk_compat import *
from promogest.ui.AnagraficaComplessa import Anagrafica
from promogest.ui.AnagraficaComplessaFilter import AnagraficaFilter
from promogest.ui.AnagraficaComplessaReport import AnagraficaReport
from promogest.ui.AnagraficaComplessaHtml import AnagraficaHtml
from promogest.ui.anagArti.AnagraficaArticoliEdit import AnagraficaArticoliEdit
from promogest.ui.anagArti.AnagraficaArticoliFilter import AnagraficaArticoliFilter
import promogest.dao.Articolo
from promogest.dao.Articolo import Articolo
import promogest.dao.Fornitura

from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
if posso("PW"):
    from promogest.modules.PromoWear.ui.PromowearUtils import *
    from promogest.modules.PromoWear.ui import AnagraficaArticoliPromoWearExpand

class AnagraficaArticoli(Anagrafica):
    """ Anagrafica articoli
    """
    def __init__(self, aziendaStr=None):
        Anagrafica.__init__(self,
                            windowTitle='Promogest - Anagrafica articoli',
                            recordMenuLabel='_Articoli',
                            filterElement=AnagraficaArticoliFilter(self),
                            htmlHandler=AnagraficaArticoliHtml(self),
                            reportHandler=AnagraficaArticoliReport(self),
                            editElement=AnagraficaArticoliEdit(self),
                            aziendaStr=aziendaStr,
                            url_help ="http://www.promogest.me/promoGest/faq_detail/come-si-inserisce-una-categoria-articolo")
        self.record_duplicate_menu.set_property('visible', True)
        self.records_file_export.set_sensitive(True)

    def on_record_edit_activate(self, widget, path=None, column=None, dao=None):
        if not dao:
            dao = self.filter.getSelectedDao()
        if dao:
            if dao.cancellato:
                msg = "L'articolo risulta eliminato.\nSi desidera riattivare l'articolo ?"
                if YesNoDialog(msg=msg, transient=self.getTopLevel()):
                    daoArticolo = Articolo().getRecord(id=dao.id)
                    daoArticolo.cancellato = False
                    daoArticolo.persist()

                    # toglie l'evidenziatura rossa
                    sel = self.anagrafica_filter_treeview.get_selection()
                    (model, iterator) = sel.get_selected()
                    model.set_value(iterator, 1, None)
            Anagrafica.on_record_edit_activate(self, widget, path, column, dao=dao)

    def duplicate(self,dao):
        """ Duplica le informazioni relative ad un articolo scelto su uno nuovo (a meno del codice)
        """
        if dao is None:
            return

        #self.editElement._duplicatedDaoId = dao.id
        self.editElement.dao = Articolo()

        if posso("PW"):
                # le varianti non si possono duplicare !!!
                #articoloTagliaColore = dao.articoloTagliaColore
                if dao.id_articolo_padre is not None:
                    messageInfo(msg="Attenzione !\n\n Le varianti non sono duplicabili !")
                    return

        #copia dei dati del vecchio articolo nel nuovo
        self.editElement.dao.denominazione = dao.denominazione
        self.editElement.dao.id_aliquota_iva = dao.id_aliquota_iva
        self.editElement.dao.id_famiglia_articolo = dao.id_famiglia_articolo
        self.editElement.dao.id_categoria_articolo = dao.id_categoria_articolo
        self.editElement.dao.id_unita_base = dao.id_unita_base
        self.editElement.dao.produttore = dao.produttore
        self.editElement.dao.unita_dimensioni = dao.unita_dimensioni
        self.editElement.dao.lunghezza = dao.lunghezza
        self.editElement.dao.larghezza = dao.larghezza
        self.editElement.dao.altezza = dao.altezza
        self.editElement.dao.unita_volume = dao.unita_volume
        self.editElement.dao.volume = dao.volume
        self.editElement.dao.unita_peso = dao.unita_peso
        self.editElement.dao.peso_lordo = dao.peso_lordo
        self.editElement.dao.id_imballaggio = dao.id_imballaggio
        self.editElement.dao.peso_imballaggio = dao.peso_imballaggio
        self.editElement.dao.stampa_etichetta = dao.stampa_etichetta
        self.editElement.dao.codice_etichetta = dao.codice_etichetta
        self.editElement.dao.descrizione_etichetta = dao.descrizione_etichetta
        self.editElement.dao.stampa_listino = dao.stampa_listino
        self.editElement.dao.descrizione_listino = dao.descrizione_listino
        self.editElement.dao.aggiornamento_listino_auto = dao.aggiornamento_listino_auto
        self.editElement.dao.timestamp_variazione = dao.timestamp_variazione
        self.editElement.dao.note = dao.note
        self.editElement.dao.url_immagine = dao.url_immagine
        self.editElement.dao.cancellato = dao.cancellato
        self.editElement.dao.sospeso = dao.sospeso
        self.editElement.dao.id_stato_articolo = dao.id_stato_articolo
        self.editElement.dao.quantita_minima = dao.quantita_minima

        if posso("ADR"):
            self.editElement.adr_page.adrSetDao(self.editElement.dao)

        if self.editElement._codiceByFamiglia:
            self.editElement.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=dao.id_famiglia_articolo)
        else:
            self.editElement.dao.codice = promogest.dao.Articolo.getNuovoCodiceArticolo(idFamiglia=None)

        self.editElement.setVisible(True)
        self.editElement._refresh()
        msg = 'Si desidera duplicare anche tutti i listini dell\' articolo scelto ?'
        if YesNoDialog(msg=msg, transient=self.editElement.dialogTopLevel):
            self.editElement._duplicatedDaoId = dao.id


class AnagraficaArticoliHtml(AnagraficaHtml):
    def __init__(self, anagrafica):
        AnagraficaHtml.__init__(self, anagrafica,
                                'articolo',
                                'Dettaglio articolo')


class AnagraficaArticoliReport(AnagraficaReport):
    def __init__(self, anagrafica):
        AnagraficaReport.__init__(self, anagrafica=anagrafica,
                                  description='Elenco degli articoli',
                                  defaultFileName='articoli',
                                  htmlTemplate='articoli',
                                  sxwTemplate='articoli')
