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

from promogest.ui.gtk_compat import *
from math import sqrt
from promogest.ui.GladeWidget import GladeWidget
from promogest import Environment
from promogest.lib.utils import *
from promogest.ui.utilsCombobox import *
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
if posso("ADR"):
    from promogest.modules.ADR.ui import AnagraficaDocumentiEditADRExt

import csv
import os
from promogest.Environment import promogestDir
def get_qta_prezzo_articoli():
    ''' Ritorna un dizionario con la quantità soglia e il nuovo prezzo
        per gli articoli leggendo da un file in formato CSV.
    '''
    filename = os.path.join(promogestDir, 'qta_prezzo.csv')
    if not os.path.isfile(filename):
        return None
    dict_art_qta_prezzo = {}
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            dict_art_qta_prezzo[row[0]] = (float(row[1]), float(row[2]))
    return dict_art_qta_prezzo

def drawPart(anaedit):
    treeview = anaedit.righe_treeview
    rendererSx = gtk.CellRendererText()
    rendererDx = gtk.CellRendererText()
    rendererDx.set_property('xalign', 1)

    column = gtk.TreeViewColumn(_('N°'), rendererSx, text=0)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn(_('Magazzino'), rendererSx, text=1)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn(_('Codice articolo'), rendererSx, text=2)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn(_('Descrizione'), rendererSx, text=3)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(True)
    treeview.append_column(column)

    column = gtk.TreeViewColumn(_('% IVA'), rendererDx, text=4)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)
    #treeview.set_reorderable(True)
    if posso("SM"):
        AnagraficaDocumentiEditSuMisuraExt.setTreeview(treeview, rendererSx)

    column = gtk.TreeViewColumn(_('Multiplo'), rendererSx, text=8)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn(_('Listino'), rendererSx, text=9)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn(_('U.M.'), rendererSx, text=10)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn(_("Quantita'"), rendererDx, text=11)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn(_('Prezzo lordo'), rendererDx, text=12)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn(_('Sconti'), rendererSx, text=13)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    column = gtk.TreeViewColumn(_('Prezzo netto'), rendererDx, text=14)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
    column.set_clickable(False)
    column.set_resizable(True)
    column.set_expand(False)
    treeview.append_column(column)

    if posso("GN"):
        AnagraficaDocumentiEditGestioneNoleggioExt.setTreeview(treeview, rendererSx)

    column = gtk.TreeViewColumn(_('Totale'), rendererDx, text=16)
    column.set_sizing(GTK_COLUMN_GROWN_ONLY)
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
    anaedit.id_persona_giuridica_customcombobox.giveAnag(anaedit)

    anaedit.id_destinazione_merce_customcombobox.connect('clicked',
            anaedit.on_id_destinazione_merce_customcombobox_button_clicked)
    anaedit.id_multiplo_customcombobox.combobox.connect('changed',
            anaedit.on_id_multiplo_customcombobox_changed)
    anaedit.id_listino_customcombobox.combobox.connect('changed',
            anaedit.on_id_listino_customcombobox_changed)
    anaedit.id_listino_customcombobox.button.connect('toggled',
            anaedit.on_id_listino_customcombobox_button_toggled)
    anaedit.id_aliquota_iva_esenzione_customcombobox.connect('clicked',
                        on_id_aliquota_iva_customcombobox_clicked)

    anaedit.id_agente_customcombobox.setHandler("agente")
    anaedit.id_vettore_customcombobox.setHandler("vettore")

    anaedit.sconti_widget.button.connect('toggled',
            anaedit.on_sconti_widget_button_toggled)
    anaedit.sconti_testata_widget.button.connect('toggled',
            anaedit.on_sconti_testata_widget_button_toggled)

def calcolaTotalePart(anaedit, dao=None):
    """ calcola i totali documento """
    # FIXME: duplicated in TestataDocumenti.py

    anaedit.avvertimento_sconti_button.set_sensitive(False)
    anaedit.avvertimento_sconti_button.hide()

    totaleImponibile = Decimal(0)
    totaleImposta = Decimal(0)
    totaleNonScontato = Decimal(0)
    totaleImpostaScontata = Decimal(0)
    totaleImponibileScontato = Decimal(0)
    totaleEsclusoBaseImponibile = Decimal(0)
    totaleScontato = Decimal(0)
    castellettoIva = {}
    totaleEsclusoBaseImponibileRiga = 0
    totaleImponibileRiga = 0

    ive = Environment.session.query(AliquotaIva.id,AliquotaIva).all()
    dictIva = {}
    for a in ive:
        dictIva[a[0]] = (a[1],a[1].tipo_ali_iva)


    gn = posso("GN")
    for riga in anaedit._righe[1:]:
        prezzoNetto = Decimal(riga["prezzoNetto"])
        quantita = Decimal(riga["quantita"])
        moltiplicatore = Decimal(riga["moltiplicatore"])
        percentualeIvaRiga = Decimal(riga["percentualeIva"])
        idAliquotaIva = riga["idAliquotaIva"]
        daoiva=None
        if idAliquotaIva:
            if idAliquotaIva in dictIva:
                daoiva = dictIva[idAliquotaIva][0]
            if daoiva:
                aliquotaIvaRiga = daoiva.percentuale
        totaleRiga = Decimal(prezzoNetto * quantita * moltiplicatore)

        # PARTE dedicata al modulo noleggio ...
        # TODO : Rivedere quanto prima
        if gn and anaedit.noleggio and str(riga["arco_temporale"]) != "NO":
            arco_temporale = Decimal(anaedit.giorni_label.get_text())
            if str(riga["divisore_noleggio"]) == "1":
                totaleRiga = mN(totaleRiga *Decimal(riga["arco_temporale"]))
            else:
                totaleRiga= mN(totaleRiga *Decimal(str(sqrt(int(riga["arco_temporale"])))))

        if (anaedit._fonteValore == "vendita_iva" or anaedit._fonteValore == "acquisto_iva"):
            if daoiva and dictIva[idAliquotaIva][1]== "Non imponibile":
                totaleEsclusoBaseImponibileRiga = totaleRiga
                totaleImponibileRiga = 0
            else:
                totaleEsclusoBaseImponibileRiga = 0
                totaleImponibileRiga = calcolaPrezzoIva(totaleRiga, -1 * percentualeIvaRiga) or 0
        else:
            if daoiva and dictIva[idAliquotaIva][1] == "Non imponibile":
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
        if daoiva:
            denominazione = daoiva.denominazione
            denominazione_breve = daoiva.denominazione_breve
        else:
            denominazione = ""
            denominazione_breve = ""

        if idAliquotaIva not in castellettoIva.keys():
            castellettoIva[idAliquotaIva] = {
                'percentuale': percentualeIvaRiga,
                'imponibile': totaleImponibileRiga,
                'imposta': totaleImpostaRiga,
                'totale': totaleRiga,
                "denominazione_breve": denominazione_breve,
                "denominazione": denominazione}
        else:
            castellettoIva[idAliquotaIva]['percentuale'] = percentualeIvaRiga
            castellettoIva[idAliquotaIva]['imponibile'] += totaleImponibileRiga
            castellettoIva[idAliquotaIva]['imposta'] += totaleImpostaRiga
            castellettoIva[idAliquotaIva]['totale'] += totaleRiga

    totaleImposta = totaleNonScontato - (totaleImponibile+totaleEsclusoBaseImponibile)
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
                    raise Exception, (_('BUG! Tipo di applicazione sconto '
                                        'sconosciuto: %s') % s['tipo'])
            elif s["tipo"] == 'valore':
                totaleImponibileScontato = totaleImponibileScontato - Decimal(s["valore"])
                if totaleImponibileScontato <0:
                    messageInfo(msg=_("TOTALE SCONTATO NON PUÒ ESSERE INFERIORE A ZERO"))
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

        totaleScontato = totaleImponibileScontato + totaleImpostaScontata
    totaleInPagamenti = totaleScontato + Decimal(str(anaedit.pagamenti_page.calcola_spese()))

    anaedit.totale_generale_label.set_text(str(mN(totaleImponibile,2) + mN(totaleImposta,2) + mN(totaleEsclusoBaseImponibile, 2)))
    anaedit.totale_generale_riepiloghi_label.set_text(str(mN(totaleImponibile,2) + mN(totaleImposta,2) + mN(totaleEsclusoBaseImponibile, 2)))
    anaedit.totale_imponibile_label.set_text(str(mN(totaleImponibileScontato, 2)))
    anaedit.totale_imponibile_riepiloghi_label.set_text(str(mN(totaleImponibile, 2)))
    anaedit.totale_imposta_label.set_text(str(mN(totaleImpostaScontata, 2)))
    anaedit.totale_imposta_riepiloghi_label.set_text(str(mN(totaleImposta, 2)))
    anaedit.totale_imponibile_scontato_riepiloghi_label.set_text(str(mN(totaleImponibileScontato, 2)))
    anaedit.totale_imposta_scontata_riepiloghi_label.set_text(str(mN(totaleImpostaScontata, 2)))
    anaedit.totale_scontato_riepiloghi_label.set_text(str(mN(totaleImponibileScontato,2) + mN(totaleImpostaScontata, 2) + mN(totaleEsclusoBaseImponibile, 2)))
    anaedit.pagamenti_page.totale_in_pagamenti_label.set_markup('<b><span foreground="black" size="24000">'+str(mN(totaleInPagamenti, 2))+'</span></b>')
    anaedit.totale_non_base_imponibile_label.set_text(str(mN(totaleEsclusoBaseImponibile, 2)))

    id_pag = anaedit._id_pagamento
    pago = Pagamento().getRecord(id=id_pag)
    if pago:
        anaedit.pagamenti_page.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+str(pago.denominazione)+'</span></b>')
    else:
        anaedit.pagamenti_page.metodo_pagamento_label.set_markup('<b><span foreground="black" size="16000">'+str(_("NESSUNO?"))+'</span></b>')

    anaedit.liststore_iva.clear()
    for k in castellettoIva.keys():
        if k !=0:
            anaedit.liststore_iva.append(((str(mN(castellettoIva[k]['percentuale'],1))),
                            (str(mN(castellettoIva[k]['imponibile'],2))),
                            (str(mN(castellettoIva[k]['imposta'],2))),))


def mostraArticoloPart(anaedit, id, art=None, quan=None):
    """questa funzione viene chiamata da ricerca articolo e si occupa di
        riempire la riga[0] con i dati corretti presi dall'articolo
    """
    data = stringToDate(anaedit.data_documento_entry.get_text())
    # articolo c'è
    if id is not None:
        #anaedit.dettaglio_giacenza_togglebutton.set_property("sensible", True)
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
            findComboboxRowFromId(anaedit.id_iva_customcombobox.combobox,
                                  anaedit._righe[0]["idAliquotaIva"])
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
        #lottiDataScadenza(idArticolo = id, data=data)
        if posso("ADR"):
            artADR = AnagraficaDocumentiEditADRExt.getADRArticolo(id)
            if artADR:
                # Aggiorna la descrizione con alcuni dati ADR
                anaedit._righe[0]["descrizione"] += "\nUN {0},, {1},, {2}, {3}".format(artADR.numero_un,
                    artADR.classe_pericolo,
                    artADR.gruppo_imballaggio,
                    artADR.galleria)
        anaedit.descrizione_entry.set_text(anaedit._righe[0]["descrizione"])

        # Recuperiamo l'aliquota preferenziale del cliente se impostata
        _id_aliquota_iva = None
        if anaedit._tipoPersonaGiuridica == "cliente":
            _id = anaedit.id_persona_giuridica_customcombobox.getId()
            if _id:
                _cliente = leggiCliente(_id)
                if _cliente and 'id_aliquota_iva' in _cliente:
                    _id_aliquota_iva = _cliente['id_aliquota_iva']
        anaedit._righe[0]["idAliquotaIva"] = _id_aliquota_iva or articolo["idAliquotaIva"]
        findComboboxRowFromId(anaedit.id_iva_customcombobox.combobox,
                              _id_aliquota_iva or anaedit._righe[0]["idAliquotaIva"])
        # Risolviamo la percentuale tramite id_iva_customcombobox
        iva = findStrFromCombobox(anaedit.id_iva_customcombobox.combobox, 0)
        if iva:
            anaedit._righe[0]["percentualeIva"] = mN(iva.percentuale, 2) or 0
        else:
            anaedit._righe[0]["percentualeIva"] = 0

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
        if quan:
            anaedit.quantita_entry.set_text(str(quan))
            anaedit._righe[0]["quantita"] = str(quan)
        if not posso("SM") and articolo["quantita_minima"]:
            anaedit.quantita_entry.set_text(str(articolo["quantita_minima"]))
            anaedit._righe[0]["quantita"] = str(articolo["quantita_minima"])

    else:
        anaedit.articolo_entry.set_text('')
        anaedit.descrizione_entry.set_text('')
        anaedit.codice_articolo_fornitore_entry.set_text('')
        anaedit.numero_lotto_entry.set_text("")
        anaedit.data_scadenza_datewidget.set_text('')
        anaedit.data_produzione_datewidget.set_text('')
        anaedit.data_prezzo_datewidget.set_text('')
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
        if anaedit.ricerca == "codice_a_barre" and setconf("Documenti", "no_ricerca_incrementale") and anaedit.nolottotemp:
            anaedit.lotto_temp_entry.grab_focus()
        else:
            anaedit.id_listino_customcombobox.combobox.grab_focus()
    elif anaedit._tipoPersonaGiuridica == "fornitore":
        anaedit.codice_articolo_fornitore_entry.grab_focus()
    else:
        anaedit.descrizione_entry.grab_focus()

def on_multi_line_button_clickedPart(anaedit, widget):
    """ widget per l'inserimento di righe "multiriga" """
    mleditor = GladeWidget(root='multi_linea_editor', path='multi_linea_editor.glade', callbacks_proxy=anaedit)
    mleditor.multi_linea_editor.set_modal(modal=True)#
    #mleditor.multi_linea_editor.set_transient_for(self)
    #self.placeWindow(mleditor.multi_linea_editor)
    desc = anaedit.descrizione_entry.get_text()
    textview_set_text(mleditor.multi_line_editor_textview, desc)
    mleditor.multi_linea_editor.show_all()
    anaedit.a = 0
    anaedit.b = 0
    def test(widget, event):
        char_count = textview_get_char_count(mleditor.multi_line_editor_textview)
        line_count = textview_get_line_count(mleditor.multi_line_editor_textview)
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
            textview_insert_at_cursor(mleditor.multi_line_editor_textview, "\n")
            anaedit.a = -1
        modified = textview_get_modified(mleditor.multi_line_editor_textview)
        textStatusBar = "Tot. Caratteri = %s , Righe = %s, Limite= %s, Colonna=%s" %(char_count,line_count, colonne, anaedit.a)
        context_id =  mleditor.multi_line_editor_statusbar.get_context_id("Multi Editor")
        mleditor.multi_line_editor_statusbar.push(context_id,textStatusBar)

    def on_ok_button_clicked(button):
        text = textview_get_text(mleditor.multi_line_editor_textview)
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
        if YesNoDialog(msg=msg, transient=None):
            anaedit.quantita_entry.set_text(str(quantita))
            QMIN = False
        else:
            anaedit.quantita_entry.set_text(str(quantita_minima))
            QMIN =True
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
