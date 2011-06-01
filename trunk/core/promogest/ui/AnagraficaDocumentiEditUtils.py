# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
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

import gtk
from math import sqrt
from GladeWidget import GladeWidget
from promogest import Environment
from utils import *
from utilsCombobox import *
from promogest.dao.Articolo import Articolo
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.DaoUtils import giacenzaArticolo
from promogest.dao.Pagamento import Pagamento

if posso("PW"):
    from promogest.modules.PromoWear.ui import AnagraficaDocumentiEditPromoWearExt
if posso("SM"):
    from promogest.modules.SuMisura.ui import AnagraficaDocumentiEditSuMisuraExt
if posso("GN"):
    from promogest.modules.GestioneNoleggio.ui import AnagraficaDocumentiEditGestioneNoleggioExt
if posso("PA"):
    from promogest.modules.Pagamenti.ui import AnagraficadocumentiPagamentExt
if posso("ADR"):
    from promogest.modules.ADR.ui import AnagraficaDocumentiEditADRExt


def drawPart(anaedit):
    treeview = anaedit.righe_treeview
    rendererSx = gtk.CellRendererText()
    rendererDx = gtk.CellRendererText()
    rendererDx.set_property('xalign', 1)

    column = gtk.TreeViewColumn('N°', rendererSx, text=0)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Magazzino', rendererSx, text=1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Codice articolo', rendererSx, text=2)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Descrizione', rendererSx, text=3)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(True)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('% IVA', rendererDx, text=4)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)
    #treeview.set_reorderable(True)
    if posso("SM"):
        AnagraficaDocumentiEditSuMisuraExt.setTreeview(treeview, rendererSx)

    column = gtk.TreeViewColumn('Multiplo', rendererSx, text=8)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Listino', rendererSx, text=9)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('U.M.', rendererSx, text=10)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Quantita''', rendererDx, text=11)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Prezzo lordo', rendererDx, text=12)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Sconti', rendererSx, text=13)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn('Prezzo netto', rendererDx, text=14)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    if posso("GN"):
        AnagraficaDocumentiEditGestioneNoleggioExt.setTreeview(treeview, rendererSx)

    column = gtk.TreeViewColumn('Totale', rendererDx, text=16)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_GROW_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)
    #treeview.set_reorderable(True)
    fillComboboxAliquoteIva(anaedit.id_iva_customcombobox.combobox)
    anaedit.id_iva_customcombobox.connect('clicked',
                                on_id_aliquota_iva_customcombobox_clicked)
    fillComboboxOperazioni(anaedit.id_operazione_combobox, 'documento')
    fillComboboxMagazzini(anaedit.id_magazzino_combobox)
    fillComboboxPagamenti(anaedit.id_pagamento_customcombobox.combobox)
    fillComboboxBanche(anaedit.id_banca_customcombobox.combobox)
    fillComboboxAliquoteIva(anaedit.id_aliquota_iva_esenzione_customcombobox.combobox)
    fillComboboxCausaliTrasporto(anaedit.causale_trasporto_comboboxentry)
    fillComboboxAspettoEsterioreBeni(anaedit.aspetto_esteriore_beni_comboboxentry)

    anaedit.id_operazione_combobox.set_wrap_width(int(setconf("Numbers", "combo_column")))

    anaedit.porto_combobox.set_active(-1)
    anaedit.porto_combobox.set_sensitive(False)
    fillComboboxNotePiePaginaTestataDocumento(anaedit.note_pie_pagina_comboboxentry)
    """ modello righe: magazzino, codice articolo,
    descrizione, percentuale iva, unita base, multiplo, listino,
    quantita, prezzo lordo, sconti, prezzo netto, totale, altezza, larghezza,molt_pezzi
    """
    anaedit.modelRiga = gtk.ListStore(int, str, str, str, str, str, str, str,\
                             str, str, str, str, str, str, str, str, str)
    anaedit.righe_treeview.set_model(anaedit.modelRiga)
    anaedit.ricerca = None
    anaedit.nuovaRiga()
    # preferenza ricerca articolo ?
    """ ATTENZIONE schifezza per tamponare il bug di gtk 2.17 numero :
        Bug 607492 - widget.get_name(): semirisolto!!!! """
    crit = setconf("Documenti", "ricerca_per")
    anaedit.ricerca = crit
    if crit == 'codice':
        anaedit.ricerca_criterio_combobox.set_active(0)
    elif crit == 'codice_a_barre':
        anaedit.ricerca_criterio_combobox.set_active(1)
    elif crit == 'descrizione':
        anaedit.ricerca_criterio_combobox.set_active(2)
    elif crit == 'codice_articolo_fornitore':
        anaedit.ricerca_criterio_combobox.set_active(3)
    if not anaedit.ricerca:
        anaedit.ricerca_criterio_combobox.set_active(2)

    anaedit.id_persona_giuridica_customcombobox.setSingleValue()
    anaedit.id_persona_giuridica_customcombobox.setOnChangedCall(anaedit.persona_giuridica_changed)

    anaedit.id_destinazione_merce_customcombobox.connect('clicked',
            anaedit.on_id_destinazione_merce_customcombobox_button_clicked)
    idHandler = anaedit.id_vettore_customcombobox.connect('changed',
            on_combobox_vettore_search_clicked)
    anaedit.id_multiplo_customcombobox.combobox.connect('changed',
            anaedit.on_id_multiplo_customcombobox_changed)
    anaedit.id_listino_customcombobox.combobox.connect('changed',
            anaedit.on_id_listino_customcombobox_changed)
    anaedit.id_listino_customcombobox.button.connect('toggled',
            anaedit.on_id_listino_customcombobox_button_toggled)
    anaedit.id_pagamento_customcombobox.connect('clicked',
                        on_id_pagamento_customcombobox_clicked)
    anaedit.id_banca_customcombobox.connect('clicked',
                        on_id_banca_customcombobox_clicked)
    anaedit.id_aliquota_iva_esenzione_customcombobox.connect('clicked',
                        on_id_aliquota_iva_customcombobox_clicked)
    anaedit.id_vettore_customcombobox.setChangedHandler(idHandler)
    idHandler = anaedit.id_agente_customcombobox.connect('changed',
            on_combobox_agente_search_clicked)
    anaedit.sconti_widget.button.connect('toggled',
            anaedit.on_sconti_widget_button_toggled)
    anaedit.sconti_testata_widget.button.connect('toggled',
            anaedit.on_sconti_testata_widget_button_toggled)

    if posso("PA"):
        # Vado a popolare anche il tab dei pagamenti
        AnagraficadocumentiPagamentExt.connectEntryPag(anaedit)


def calcolaTotalePart(anaedit, dao=None):
    """ calcola i totali documento """
    # FIXME: duplicated in TestataDocumenti.py
    totaleImponibile = Decimal(0)
    totaleImposta = Decimal(0)
    totaleNonScontato = Decimal(0)
    totaleImpostaScontata = Decimal(0)
    totaleImponibileScontato = Decimal(0)
    totaleEsclusoBaseImponibile = Decimal(0)
    totaleScontato = Decimal(0)
    castellettoIva = {}

    anaedit.avvertimento_sconti_button.set_sensitive(False)
    anaedit.avvertimento_sconti_button.hide()

    totaleEsclusoBaseImponibileRiga = 0
    totaleImponibileRiga = 0
    for riga in anaedit._righe[1:]:
        prezzoNetto = Decimal(riga["prezzoNetto"])
        quantita = Decimal(riga["quantita"])
        moltiplicatore = Decimal(riga["moltiplicatore"])
        percentualeIva = Decimal(riga["percentualeIva"])
        idAliquotaIva = riga["idAliquotaIva"]
        daoiva=None
        if idAliquotaIva:
            daoiva = AliquotaIva().getRecord(id=idAliquotaIva)
        totaleRiga = Decimal(prezzoNetto * quantita * moltiplicatore)

        # PARTE dedicata al modulo noleggio ...
        # TODO : Rivedere quanto prima
        if posso("GN") and anaedit.noleggio and str(riga["arco_temporale"]) != "NO":
            arco_temporale = Decimal(anaedit.giorni_label.get_text())
            if str(riga["divisore_noleggio"]) == "1":
                totaleRiga = mN(totaleRiga *Decimal(riga["arco_temporale"]))
            else:
                totaleRiga= mN(totaleRiga *Decimal(str(sqrt(int(riga["arco_temporale"])))))

        percentualeIvaRiga = percentualeIva

        if (anaedit._fonteValore == "vendita_iva" or anaedit._fonteValore == "acquisto_iva"):
            if daoiva and daoiva.tipo_ali_iva == "Non imponibile":
                totaleEsclusoBaseImponibileRiga = totaleRiga
                totaleImponibileRiga = 0
            else:
                totaleEsclusoBaseImponibileRiga = 0
                totaleImponibileRiga = calcolaPrezzoIva(totaleRiga, -1 * percentualeIvaRiga) or 0
        else:
            if daoiva and daoiva.tipo_ali_iva == "Non imponibile":
                totaleEsclusoBaseImponibileRiga = totaleRiga
                totaleImponibileRiga = 0
                totaleRiga = calcolaPrezzoIva(totaleRiga, percentualeIvaRiga)
            else:
                totaleEsclusoBaseImponibileRiga = 0
                totaleImponibileRiga = totaleRiga
                totaleRiga = calcolaPrezzoIva(totaleRiga, percentualeIvaRiga)
        totaleImpostaRiga = totaleRiga - (totaleImponibileRiga+totaleEsclusoBaseImponibileRiga)
        totaleNonScontato += totaleRiga
        totaleImponibile += totaleImponibileRiga
        totaleImposta += totaleImpostaRiga
        totaleEsclusoBaseImponibile += totaleEsclusoBaseImponibileRiga

        if percentualeIvaRiga not in castellettoIva.keys():

            castellettoIva[percentualeIvaRiga] = {'percentuale': percentualeIvaRiga,
                                                'imponibile': totaleImponibileRiga,
                                                'imposta': totaleImpostaRiga,
                                                'totale': totaleRiga}
        else:
            castellettoIva[percentualeIvaRiga]['percentuale'] = percentualeIvaRiga
            castellettoIva[percentualeIvaRiga]['imponibile'] += totaleImponibileRiga
            castellettoIva[percentualeIvaRiga]['imposta'] += totaleImpostaRiga
            castellettoIva[percentualeIvaRiga]['totale'] += totaleRiga

#    totaleNonScontato = totaleNonScontato
#    totaleImponibile = totaleImponibile
    totaleImposta = totaleNonScontato - (totaleImponibile+totaleEsclusoBaseImponibile)
#    totaleEsclusoBaseImponibile = totaleEsclusoBaseImponibile
#    for percentualeIva in castellettoIva: #????????????????????????
#        castellettoIva[percentualeIva]['imponibile'] = castellettoIva[percentualeIva]['imponibile']
#        castellettoIva[percentualeIva]['imposta'] = castellettoIva[percentualeIva]['imposta']
#        castellettoIva[percentualeIva]['totale'] = castellettoIva[percentualeIva]['totale']


    totaleImponibileScontato = totaleImponibile
    totaleImpostaScontata = totaleImposta
    totaleScontato = totaleNonScontato
    scontiSuTotale = anaedit.sconti_testata_widget.getSconti()
    applicazioneSconti = anaedit.sconti_testata_widget.getApplicazione()

    if len(scontiSuTotale) > 0:
        anaedit.avvertimento_sconti_button.set_sensitive(True)
        anaedit.avvertimento_sconti_button.show()
        for s in scontiSuTotale:
            if s["tipo"] == 'percentuale':
                if applicazioneSconti == 'scalare':
                    totaleImponibileScontato = totaleImponibileScontato * (1 - Decimal(s["valore"]) / 100)
                elif applicazioneSconti == 'non scalare':
                    totaleImponibileScontato = totaleImponibileScontato - totaleImponibile * Decimal(s["valore"]) / 100
                else:
                    raise Exception, ('BUG! Tipo di applicazione sconto '
                                        'sconosciuto: %s' % s['tipo'])
            elif s["tipo"] == 'valore':
                totaleImponibileScontato = totaleImponibileScontato - Decimal(s["valore"])
                if totaleImponibileScontato <0:
                    messageInfo(msg="TOTALE SCONTATO NON PUÒ ESSERE INFERIORE A ZERO")
                    anaedit.sconti_testata_widget.setValues([])
                    return

        # riporta l'insieme di sconti ad una percentuale globale
        if totaleScontato >0:
            percentualeScontoGlobale = (1 - totaleImponibileScontato / totaleImponibile) * 100
        else:
            percentualeScontoGlobale = 100

        totaleImpostaScontata = 0
        totaleImponibileScontato = 0
#        totaleScontato = 0
        # riproporzione del totale, dell'imponibile e dell'imposta

        for k in castellettoIva.keys():
            castellettoIva[k]['totale'] = Decimal(castellettoIva[k]['totale']) * (1 - Decimal(percentualeScontoGlobale) / 100)
            castellettoIva[k]['imponibile'] = Decimal(castellettoIva[k]['imponibile']) * (1 - Decimal(percentualeScontoGlobale) / 100)
            castellettoIva[k]['imposta'] = castellettoIva[k]['totale'] - castellettoIva[k]['imponibile']

            totaleImponibileScontato += Decimal(castellettoIva[k]['imponibile'])
            totaleImpostaScontata += Decimal(castellettoIva[k]['imposta'])

        totaleScontato = Decimal(totaleImponibileScontato) + Decimal(totaleImpostaScontata)
    anaedit.totale_generale_label.set_text(str(mN(totaleScontato,2)))
    anaedit.totale_generale_riepiloghi_label.set_text(str(mN(totaleNonScontato,2)))
    anaedit.totale_imponibile_label.set_text(str(mN(totaleImponibileScontato, 2)))
    anaedit.totale_imponibile_riepiloghi_label.set_text(str(mN(totaleImponibile,2)))
    anaedit.totale_imposta_label.set_text(str(mN(totaleImpostaScontata, 2)))
    anaedit.totale_imposta_riepiloghi_label.set_text(str(mN(totaleImposta, 2)))
    anaedit.totale_imponibile_scontato_riepiloghi_label.set_text(str(mN(totaleImponibileScontato, 2)))
    anaedit.totale_imposta_scontata_riepiloghi_label.set_text(str(mN(totaleImpostaScontata, 2)))
    anaedit.totale_scontato_riepiloghi_label.set_text(str(mN(totaleScontato, 2)))
    anaedit.totale_in_pagamenti_label.set_markup('<b><span foreground="black" size="24000">'+str(mN(totaleScontato,2))+'</span></b>')
    anaedit.totale_non_base_imponibile_label.set_text(str(mN(totaleEsclusoBaseImponibile,2)))

    id_pag = anaedit._id_pagamento
    pago = Pagamento().getRecord(id=id_pag)
    if pago:
        anaedit.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+str(pago.denominazione)+'</span></b>')
    else:
        anaedit.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+str("NESSUNO?")+'</span></b>')

    anaedit.liststore_iva.clear()
    for k in castellettoIva.keys():
        if k !=0:
            anaedit.liststore_iva.append((str(mN(k,1)),
                            (str(mN(castellettoIva[k]['imponibile'],2))),
                            (str(mN(castellettoIva[k]['imposta'],2))),))


def mostraArticoloPart(anaedit, id, art=None):
    """questa funzione viene chiamata da ricerca articolo e si occupa di
        riempire la riga[0] con i dati corretti presi dall'articolo
    """
    data = stringToDate(anaedit.data_documento_entry.get_text())
    # articolo c'è
    if id is not None:
        fillComboboxMultipli(anaedit.id_multiplo_customcombobox.combobox, id, True)
        articolo = leggiArticolo(id)
        if posso("PW"):
            AnagraficaDocumentiEditPromoWearExt.fillLabelInfo(anaedit, articolo)
        artic = Articolo().getRecord(id=id)
        if articleType(artic) =="father":
            anaedit.ArticoloPadre = artic
            anaedit.promowear_manager_taglia_colore_togglebutton.set_property("visible", True)
            anaedit.promowear_manager_taglia_colore_togglebutton.set_sensitive(True)
#            anaedit.on_promowear_manager_taglia_colore_togglebutton_toggled(anaedit)
            anaedit.NoRowUsableArticle = True
        if art:
            # articolo proveninente da finestra taglia e colore ...
            anaedit.NoRowUsableArticle = False
            articolo = art
            anaedit._righe[0]["idArticolo"] = id
            anaedit._righe[0]["codiceArticolo"] = articolo["codice"]
            anaedit.articolo_entry.set_text(anaedit._righe[0]["codiceArticolo"])
            anaedit._righe[0]["descrizione"] = articolo["denominazione"]
            anaedit.descrizione_entry.set_text(anaedit._righe[0]["descrizione"])
            anaedit._righe[0]["percentualeIva"] = mN(articolo["percentualeAliquotaIva"],2)
#ATTENZIONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!
            anaedit._righe[0]["idAliquotaIva"] = articolo["idAliquotaIva"]
            findComboboxRowFromId(anaedit.id_iva_customcombobox.combobox,anaedit._righe[0]["idAliquotaIva"])
#            anaedit.percentuale_iva_entry.set_text(str(anaedit._righe[0]["percentualeIva"]))
            anaedit._righe[0]["idUnitaBase"] = articolo["idUnitaBase"]
            anaedit._righe[0]["unitaBase"] = articolo["unitaBase"]
            anaedit.unitaBaseLabel.set_text(anaedit._righe[0]["unitaBase"])
            if ((anaedit._fonteValore == "acquisto_iva") or  (anaedit._fonteValore == "acquisto_senza_iva")):
                costoLordo = str(articolo['valori']["prezzoLordo"])
                if costoLordo:
                    costoLordo = costoLordo.replace(',', '.')
                costoNetto = str(articolo['valori']["prezzoNetto"])
                if costoNetto:
                    costoNetto = costoNetto.replace(',', '.')
                if anaedit._fonteValore == "acquisto_iva":
                    costoLordo = calcolaPrezzoIva(costoLordo, anaedit._righe[0]["percentualeIva"])
                    costoNetto = calcolaPrezzoIva(costoNetto, anaedit._righe[0]["percentualeIva"])
                anaedit._righe[0]["prezzoLordo"] = mN(costoLordo)
                anaedit.prezzo_lordo_entry.set_text(str(anaedit._righe[0]["prezzoLordo"]))
                anaedit._righe[0]["prezzoNetto"] = mN(costoNetto)
                anaedit.prezzo_netto_label.set_text(str(anaedit._righe[0]["prezzoNetto"]))
                anaedit._righe[0]["prezzoNettoUltimo"] = mN(costoNetto)
                anaedit._righe[0]["sconti"] = articolo['valori']["sconti"]
                anaedit._righe[0]["applicazioneSconti"] = articolo['valori']["applicazioneSconti"]
                anaedit.sconti_widget.setValues(anaedit._righe[0]["sconti"], anaedit._righe[0]["applicazioneSconti"], False)
                anaedit._righe[0]["codiceArticoloFornitore"] = articolo['valori']["codiceArticoloFornitore"]
                anaedit.codice_articolo_fornitore_entry.set_text(anaedit._righe[0]["codiceArticoloFornitore"])
                quantita =articolo["quantita"]
                quantita = quantita.replace(',','.')
                anaedit._righe[0]["quantita"] = quantita
                anaedit.quantita_entry.set_text(anaedit._righe[0]["quantita"])
                if anaedit._righe[0]["quantita"]:
                    anaedit.calcolaTotaleRiga()
            elif anaedit._fonteValore == "vendita_iva":

                costoLordo = str(articolo['valori']["prezzoDettaglio"])
                if costoLordo:
                    costoLordo = costoLordo.replace(',','.')
                anaedit._righe[0]["prezzoLordo"] = mN(costoLordo)
                anaedit.prezzo_lordo_entry.set_text(str(anaedit._righe[0]["prezzoLordo"]))
                anaedit._righe[0]["sconti"] = articolo['valori']["scontiDettaglio"]
                anaedit._righe[0]["applicazioneSconti"] = articolo['valori']["applicazioneScontiDettaglio"]
                anaedit.sconti_widget.setValues(anaedit._righe[0]["sconti"], anaedit._righe[0]["applicazioneSconti"], False)
                quantita =articolo["quantita"]
                quantita = quantita.replace(',', '.')
                anaedit._righe[0]["quantita"] = quantita
                anaedit.quantita_entry.set_text(anaedit._righe[0]["quantita"])
                if anaedit._righe[0]["quantita"]:
                    anaedit.calcolaTotaleRiga()
                anaedit.on_show_totali_riga()
                #anaedit.refresh_combobox_listini()
            elif anaedit._fonteValore == "vendita_senza_iva":
                costoLordo = str(articolo['valori']["prezzoIngrosso"])
                if costoLordo:
                    costoLordo = costoLordo.replace(',','.')
                anaedit._righe[0]["prezzoLordo"] = mN(costoLordo)
                anaedit.prezzo_lordo_entry.set_text(str(anaedit._righe[0]["prezzoLordo"]))
                anaedit._righe[0]["sconti"] = articolo['valori']["scontiIngrosso"]
                anaedit._righe[0]["applicazioneSconti"] = articolo['valori']["applicazioneScontiIngrosso"]
                anaedit.sconti_widget.setValues(anaedit._righe[0]["sconti"], anaedit._righe[0]["applicazioneSconti"], False)
                quantita =articolo["quantita"]
                quantita = quantita.replace(',','.')
                anaedit._righe[0]["quantita"] = quantita
                anaedit.quantita_entry.set_text(anaedit._righe[0]["quantita"])
                if anaedit._righe[0]["quantita"]:
                    anaedit.calcolaTotaleRiga()
                anaedit.on_show_totali_riga()

            anaedit.on_confirm_row_button_clicked(anaedit.dialogTopLevel)
            return
        #Eccoci all'articolo normale
        anaedit._righe[0]["idArticolo"] = id
        anaedit._righe[0]["codiceArticolo"] = articolo["codice"]
        anaedit.articolo_entry.set_text(anaedit._righe[0]["codiceArticolo"])
        anaedit._righe[0]["descrizione"] = articolo["denominazione"]
        if posso("ADR"):
            artADR = AnagraficaDocumentiEditADRExt.getADRArticolo(id)
            if artADR:
                # Aggiorna la descrizione con alcuni dati ADR
                anaedit._righe[0]["descrizione"] += "\nUN {0},, {1},, {2}, {3}".format(artADR.numero_un,
                    artADR.classe_pericolo,
                    artADR.gruppo_imballaggio,
                    artADR.galleria)
        anaedit.descrizione_entry.set_text(anaedit._righe[0]["descrizione"])
        anaedit._righe[0]["percentualeIva"] = mN(articolo["percentualeAliquotaIva"],2)
        anaedit._righe[0]["idAliquotaIva"] = articolo["idAliquotaIva"]
        findComboboxRowFromId(anaedit.id_iva_customcombobox.combobox,anaedit._righe[0]["idAliquotaIva"])
#        anaedit.percentuale_iva_entry.set_text(str(anaedit._righe[0]["percentualeIva"]))
        anaedit._righe[0]["idUnitaBase"] = articolo["idUnitaBase"]
        anaedit._righe[0]["unitaBase"] = articolo["unitaBase"]
        anaedit.unitaBaseLabel.set_text(anaedit._righe[0]["unitaBase"])
        anaedit._righe[0]["idMultiplo"] = None
        anaedit._righe[0]["moltiplicatore"] = 1

        if posso("GN") and anaedit.noleggio:
            anaedit._righe[0]["divisore_noleggio"] = artic.divisore_noleggio
            anaedit.coeficente_noleggio_entry.set_text(str(anaedit._righe[0]["divisore_noleggio"]))
            anaedit._getPrezzoAcquisto()

        anaedit._righe[0]["prezzoLordo"] = 0
        anaedit._righe[0]["prezzoNetto"] = 0
        anaedit._righe[0]["sconti"] = []
        anaedit._righe[0]["applicazioneSconti"] = 'scalare'
        anaedit._righe[0]["codiceArticoloFornitore"] = artic.codice_articolo_fornitore
        #inserisco dei dati nel frame delle informazioni
        anaedit.giacenza_label.set_text(str(giacenzaArticolo(year=Environment.workingYear,
                                            idMagazzino=findIdFromCombobox(anaedit.id_magazzino_combobox),
                                            idArticolo=anaedit._righe[0]["idArticolo"])))

        anaedit.quantitaMinima_label.set_text(str(artic.quantita_minima))
        # Acquisto
        if ((anaedit._fonteValore == "acquisto_iva") or  (anaedit._fonteValore == "acquisto_senza_iva")):
            fornitura = leggiFornitura(id, anaedit.id_persona_giuridica_customcombobox.getId(), data)
            costoLordo = fornitura["prezzoLordo"]
            costoNetto = fornitura["prezzoNetto"]
            if anaedit._fonteValore == "acquisto_iva":
                    costoLordo = calcolaPrezzoIva(costoLordo,
                                            anaedit._righe[0]["percentualeIva"])
                    costoNetto = calcolaPrezzoIva(costoNetto,
                                            anaedit._righe[0]["percentualeIva"])
            anaedit._righe[0]["prezzoLordo"] = costoLordo
            anaedit.prezzo_lordo_entry.set_text(str(anaedit._righe[0]["prezzoLordo"]))
            anaedit._righe[0]["prezzoNetto"] = costoNetto
            anaedit.prezzo_netto_label.set_text(str(anaedit._righe[0]["prezzoNetto"]))
            anaedit._righe[0]["prezzoNettoUltimo"] = costoNetto
            anaedit._righe[0]["sconti"] = fornitura["sconti"]
            anaedit._righe[0]["applicazioneSconti"] = fornitura["applicazioneSconti"]
            anaedit.sconti_widget.setValues(anaedit._righe[0]["sconti"], anaedit._righe[0]["applicazioneSconti"], False)
#            anaedit._righe[0]["codiceArticoloFornitore"] = fornitura["codiceArticoloFornitore"]
            anaedit.codice_articolo_fornitore_entry.set_text(anaedit._righe[0]["codiceArticoloFornitore"] or "")
        #vendita
        elif ((anaedit._fonteValore == "vendita_iva") or (anaedit._fonteValore == "vendita_senza_iva")):
            anaedit.refresh_combobox_listini()
    else:
        anaedit.articolo_entry.set_text('')
        anaedit.descrizione_entry.set_text('')
        anaedit.codice_articolo_fornitore_entry.set_text('')
        anaedit.numero_lotto_entry.set_text("")
        anaedit.data_scadenza_datewidget.set_text('')
        anaedit.ordine_minimo_entry.set_text('')
        anaedit.tempo_arrivo_merce_entry.set_text('')
#        anaedit.percentuale_iva_entry.set_text('0')
        anaedit.id_iva_customcombobox.combobox.set_active(-1)
        anaedit.id_multiplo_customcombobox.combobox.clear()
        anaedit.id_listino_customcombobox.combobox.clear()
        anaedit.prezzo_lordo_entry.set_text('0')
        anaedit.quantita_entry.set_text('0')
        anaedit.prezzo_netto_label.set_text('0')
        anaedit.sconti_widget.clearValues()
        anaedit.totale_riga_label.set_text('0')

        anaedit._righe[0]["idArticolo"] = None
        anaedit._righe[0]["codiceArticolo"] = ''
        anaedit._righe[0]["descrizione"] = ''
        anaedit._righe[0]["codiceArticoloFornitore"] = ''
        anaedit._righe[0]["percentualeIva"] = 0
        anaedit._righe[0]["idAliquotaIva"] = None
        anaedit._righe[0]["idUnitaBase"] = None
        anaedit._righe[0]["idMultiplo"] = None
        anaedit._righe[0]["moltiplicatore"] = 1
        anaedit._righe[0]["idListino"] = None
        anaedit._righe[0]["prezzoLordo"] = 0
        anaedit._righe[0]["quantita"] = 0
        anaedit._righe[0]["prezzoNetto"] = 0
        anaedit._righe[0]["divisore_noleggio"] = 0
        anaedit._righe[0]["sconti"] = []
        anaedit._righe[0]["applicazioneSconti"] = 'scalare'
        anaedit._righe[0]["totale"] = 0

    if anaedit._tipoPersonaGiuridica == "cliente":
        anaedit.id_listino_customcombobox.combobox.grab_focus()
    elif anaedit._tipoPersonaGiuridica == "fornitore":
        anaedit.codice_articolo_fornitore_entry.grab_focus()
    else:
        anaedit.descrizione_entry.grab_focus()

def on_multi_line_button_clickedPart(anaedit, widget):
    """ widget per l'inserimento di righe "multiriga" """
    mleditor = GladeWidget('multi_linea_editor', callbacks_proxy=anaedit)
    mleditor.multi_linea_editor.set_modal(modal=True)#
    #mleditor.multi_linea_editor.set_transient_for(self)
    #self.placeWindow(mleditor.multi_linea_editor)
    desc = anaedit.descrizione_entry.get_text()
    textBuffer = mleditor.multi_line_editor_textview.get_buffer()
    textBuffer.set_text(desc)
    mleditor.multi_line_editor_textview.set_buffer(textBuffer)
    mleditor.multi_linea_editor.show_all()
    anaedit.a = 0
    anaedit.b = 0
    def test(widget, event):
        char_count = textBuffer.get_char_count()
        line_count = textBuffer.get_line_count()
        if char_count >= 500:
            on_ok_button_clicked(button)
        if anaedit.b != line_count:
            anaedit.b = line_count
            anaedit.a = -1
        anaedit.a += 1
        colonne = int(setconf("Multilinea","multilinealimite"))
        if anaedit.a <= (int(setconf("Multilinea","multilinealimite"))-1):
            pass
        else:
            textBuffer.insert_at_cursor("\n")
            anaedit.a = -1
        modified = textBuffer.get_modified()
        textStatusBar = "Tot. Caratteri = %s , Righe = %s, Limite= %s, Colonna=%s" %(char_count,line_count, colonne, anaedit.a)
        context_id =  mleditor.multi_line_editor_statusbar.get_context_id("Multi Editor")
        mleditor.multi_line_editor_statusbar.push(context_id,textStatusBar)

    def on_ok_button_clicked(button):
        text = textBuffer.get_text(textBuffer.get_start_iter(),
                                    textBuffer.get_end_iter())

        anaedit.descrizione_entry.set_text(text)
        vediamo = anaedit.descrizione_entry.get_text()
        mleditor.multi_linea_editor.hide()
    button = mleditor.ok_button
    button.connect("clicked", on_ok_button_clicked)
    mleditor.multi_line_editor_textview.connect("key-press-event", test)

QMIN = False

def on_moltiplicatore_entry_focus_out_eventPart(anaedit, entry, event):
    """ funzione di controllo per quantià superiori a uno """
    from promogest.modules.SuMisura.ui.SuMisura import CalcolaArea, CalcolaPerimetro
    altezza = float(anaedit.altezza_entry.get_text() or 0)
    molti = float(anaedit.moltiplicatore_entry.get_text() or 1)
    larghezza = float(anaedit.larghezza_entry.get_text() or 0)
    quantita = None
    if anaedit._righe[0]["unitaBase"] == "Metri Quadri":
        quantita = CalcolaArea(altezza, larghezza)
    elif anaedit._righe[0]["unitaBase"] == "Metri":
        quantita = CalcolaPerimetro(altezza, larghezza)
    if quantita:
        da_stamp = molti * float(quantita)
        anaedit.quantita_entry.set_text(str(da_stamp))
    on_quantita_entry_focus_out_eventPart(anaedit, anaedit.quantita_entry, event=None)
#    anaedit.on_show_totali_riga(anaedit)


def on_quantita_entry_focus_out_eventPart(anaedit, entry, event=None):
    """ Funzione di controllo della quantità minima con dialog """

    quantita = float(anaedit.quantita_entry.get_text())
    id = anaedit._righe[0]["idArticolo"]
    if id is not None:
        articolo = Articolo().getRecord(id=id)
    else:
        return
    molti = anaedit.moltiplicatore_entry.get_text() #pezzi
    pezzi = 0
    if molti and float(molti) >0: #se pezzi è maggiore di uno o esiste vuol dire che suMisura è attivo
        pezzi = float(molti)
        if articolo:
            try:
                quantita_minima = float(articolo.quantita_minima) *pezzi
            except:
                quantita_minima = None
    else:
        if articolo:
            try:
                quantita_minima = float(articolo.quantita_minima)
            except:
                quantita_minima = None
    if quantita_minima and quantita < quantita_minima :
        msg = """Attenzione!
La quantità inserita:  %s è inferiore
a %s definita come minima di default.
Inserire comunque?""" % (str(quantita), str(quantita_minima))

        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO, msg)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_NONE or response == gtk.RESPONSE_NO:
            anaedit.quantita_entry.set_text(str(quantita_minima))
            QMIN =True
        elif response == gtk.RESPONSE_YES:
            anaedit.quantita_entry.set_text(str(quantita))
            QMIN = False
    anaedit.on_show_totali_riga(anaedit)


def hidePromoWear(ui):
    """ Hide and destroy labels and button if promowear is not present """
    ui.promowear_manager_taglia_colore_togglebutton.destroy()
    ui.promowear_manager_taglia_colore_image.hide()
    ui.anno_label.destroy()
    ui.label_anno.destroy()
    ui.stagione_label.destroy()
    ui.label15.destroy()
    ui.colore_label.destroy()
    ui.label14.destroy()
    ui.taglia_label.destroy()
    ui.label_taglia.destroy()
    ui.gruppo_taglia_label.destroy()
    ui.label_gruppo_taglia.destroy()
    ui.tipo_label.destroy()
    ui.label_tipo.destroy()


def hideSuMisura(ui):
    """funzione per SuMisura .....rimuove dalla vista quando modulo è disattivato
    """
    ui.sumisura_hbox.destroy()
    ui.moltiplicatore_entry.destroy()
    ui.label_moltiplicatore.hide()

def hideADR(ui):
    ui.adr_frame.destroy()
