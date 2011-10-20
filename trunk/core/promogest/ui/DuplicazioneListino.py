# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
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


import datetime
from GladeWidget import GladeWidget
from promogest import Environment
from decimal import *
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.ListinoCategoriaCliente import ListinoCategoriaCliente
from promogest.dao.ListinoComplessoListino import ListinoComplessoListino
from promogest.dao.ListinoMagazzino import ListinoMagazzino
from utils import *


class DuplicazioneListino(GladeWidget):

    def __init__(self, daoListino, anagraficaListino):

        self.dao = daoListino
        GladeWidget.__init__(self, 'duplicazione_listino_window',
                                    'duplicazione_listino.glade')
        self.placeWindow(self.getTopLevel())
        self.dati_vecchio_listino_label.set_text(self.dao.denominazione + \
                        " DEL: "+ dateTimeToString(self.dao.data_listino))


    def on_confirms_button_clicked(self, button):
        if self.data_listino_duplicato_entry.get_text() == '':
            obligatoryField(self.getTopLevel(),
                                 self.data_listino_duplicato_entry)
        if (self.nome_listino_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel, self.nome_listino_entry)

        if (self.descrizione_listino_entry.get_text() == ''):
            obligatoryField(self.dialogTopLevel,
                                            self.descrizione_listino_entry)

        tutto = self.tutto_duplicato_check.get_active()
        tieni_data = self.tieni_data_check.get_active()
        sconto = self.duplica_listini_scontowidget.get_text()
        tiposconto = self.duplica_listini_scontowidget.tipoSconto
        plus = self.plus_radio.get_active()

        newDao = Listino()
        newDao.data_listino = stringToDate(self.data_listino_duplicato_entry.get_text())
        newDao.denominazione = self.nome_listino_entry.get_text()
        newDao.descrizione = self.descrizione_listino_entry.get_text()
        if tutto:
            newDao.listino_attuale = True
            newDao.visible = True
        if Environment.tipo_eng !="sqlite" and not newDao.id:
            listino_sequence = Sequence("listino_id_seq",
                                        schema=Environment.params['schema'])
            newDao.id = Environment.params['session'].connection().execute(listino_sequence)
        if Environment.tipo_eng =="sqlite" and not newDao.id:
            listini = Listino().select(orderBy=Listino.id, batchSize=None)
            if not listini:
                newDao.id = 1
            else:
                newDao.id = max([p.id for p in listini]) +1
        newDao.persist()

        lcc = ListinoCategoriaCliente().select(idListino=self.dao.id,
                                                        batchSize=None)
        if lcc:
            for l in lcc:
                lccdao = ListinoCategoriaCliente()
                lccdao.id_listino = newDao.id
                lccdao.id_categoria_cliente = l.id_categoria_cliente
                lccdao.persist()

        lcl = ListinoComplessoListino().select(idListino=self.dao.id,
                                                            batchSize=None)
        if lcl:
            for l in lcl:
                lcldao = ListinoComplessoListino()
                lcldao.id_listino = newDao.id
                lcldao.id_listino_complesso = l.id_listino_complesso
                lcldao.persist()

        lm = ListinoMagazzino().select(idListino=self.dao.id, batchSize=None)
        if lm:
            for l in lm:
                lmdao = ListinoMagazzino()
                lmdao.id_listino = newDao.id
                lmdao.id_magazzino = l.id_magazzino
                lmdao.persist()

        la = ListinoArticolo().select(idListino= self.dao.id, batchSize=None)
        if la:
            for l in la:
                ladao = ListinoArticolo()
                ladao.id_listino = newDao.id
                ladao.id_articolo = l.id_articolo
                if sconto:
                    if tiposconto == "percentuale":
                        if plus:
                            ladao.prezzo_dettaglio = l.prezzo_dettaglio + (l.prezzo_dettaglio * Decimal(sconto) / 100)
                            ladao.prezzo_ingrosso = l.prezzo_ingrosso +(l.prezzo_ingrosso * Decimal(sconto) / 100)
#                            ladao.ultimo_costo = l.ultimo_costo + (l.ultimo_costo * Decimal(sconto) / 100)
                        else:
                            ladao.prezzo_dettaglio = l.prezzo_dettaglio - (l.prezzo_dettaglio * Decimal(sconto) / 100)
                            ladao.prezzo_ingrosso = l.prezzo_ingrosso -(l.prezzo_ingrosso * Decimal(sconto) / 100)
#                            ladao.ultimo_costo = l.ultimo_costo -(l.ultimo_costo * Decimal(sconto) / 100)
                    else:
                        if plus:
                            ladao.prezzo_dettaglio = l.prezzo_dettaglio + Decimal(sconto)
                            ladao.prezzo_ingrosso = l.prezzo_ingrosso + Decimal(sconto)
#                            ladao.ultimo_costo = l.ultimo_costo + Decimal(sconto)
                        else:
                            ladao.prezzo_dettaglio = l.prezzo_dettaglio - Decimal(sconto)
                            ladao.prezzo_ingrosso = l.prezzo_ingrosso - Decimal(sconto)
#                            ladao.ultimo_costo = l.ultimo_costo - Decimal(sconto)
                else:
                    ladao.prezzo_dettaglio = l.prezzo_dettaglio
                    ladao.prezzo_ingrosso = l.prezzo_ingrosso
                ladao.ultimo_costo = l.ultimo_costo
                if tieni_data:
                    ladao.data_listino_articolo = l.data_listino_articolo
                else:
                    ladao.data_listino_articolo = datetime.datetime.now()
                ladao.listino_attuale = True
                Environment.session.add(ladao)
            Environment.session.commit()

        messageInfo(msg="Nuovo Listino creato")

        self.getTopLevel().hide()

    def on_chiudi_button_clicked(self, widget, event=None):
        self.getTopLevel().hide()
        return None
