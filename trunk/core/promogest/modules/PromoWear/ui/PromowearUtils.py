# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


#import promogest.modules.PromoWear.dao.ArticoloPromowear
from promogest.modules.PromoWear.dao.ArticoloPromowear import Articolo
from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.modules.PromoWear.dao.Taglia import Taglia
from promogest.modules.PromoWear.dao.Colore import Colore
from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento
import promogest.dao.Listino
from promogest.ui.utils import findIdFromCombobox, findComboboxRowFromId
from promogest import Environment
import gtk
import gobject


def leggiArticolo(id):
    # restituisce un dizionario con le informazioni sull'articolo letto
    _id = None
    _denominazione = ''
    _codice = ''
    _denominazioneBreveAliquotaIva = ''
    _percentualeAliquotaIva = 0
    _idUnitaBase = None
    _unitaBase = ''
    _idGruppoTaglia = None
    _gruppoTaglia = ''
    _idTaglia = None
    _taglia = ''
    _idColore = None
    _colore = ''
    _idAnno = None
    _anno = ''
    _idStagione = None
    _stagione = ''
    _idGenere = None
    _genere = ''

    if id is not None:
        daoArticolo = Articolo(id=id).getRecord()
        if daoArticolo is not None:
            _id = id
            _denominazione = daoArticolo.denominazione or ''
            _codice = daoArticolo.codice or ''
            _idUnitaBase = daoArticolo.id_unita_base
            if _idUnitaBase is not None:
                #queryString = ("SELECT * FROM promogest.unita_base WHERE id = '" + str(_idUnitaBase) + "'")
                #argList = []
                #Environment.connection._cursor.execute(queryString, argList)
                #res = Environment.connection._cursor.fetchall()
                res = UnitaBase(isList=True).select(batchSize=None)
                if res is not None:
                    _unitaBase = res[0].denominazione
            if daoArticolo.id_aliquota_iva is not None:
                daoAliquotaIva = AliquotaIva(id=daoArticolo.id_aliquota_iva).getRecord()
                if daoAliquotaIva is not None:
                    _denominazioneBreveAliquotaIva = daoAliquotaIva.denominazione_breve or ''
                    _percentualeAliquotaIva = daoAliquotaIva.percentuale or 0
            if "PromoWear" in Environment.modulesList and Enviroment.taglia_colore:
                daoArticoloTagliaColore = daoArticolo
                if daoArticoloTagliaColore is not None:
                    _idGruppoTaglia = daoArticoloTagliaColore.id_gruppo_taglia
                    _gruppoTaglia = daoArticoloTagliaColore.denominazione_gruppo_taglia or '-'
                    _idtaglia = daoArticoloTagliaColore.id_taglia
                    _taglia = daoArticoloTagliaColore.denominazione_taglia or '-'
                    _idColore = daoArticoloTagliaColore.id_colore
                    _colore = daoArticoloTagliaColore.denominazione_colore or '-'
                    _idAnno = daoArticoloTagliaColore.id_anno
                    _anno = daoArticoloTagliaColore.anno or '-'
                    _idStagione = daoArticoloTagliaColore.id_stagione
                    _stagione = daoArticoloTagliaColore.stagione or '-'
                    _idGenere = daoArticoloTagliaColore.id_genere
                    _genere = daoArticoloTagliaColore.genere or '-'

    return {"id": _id,
            "denominazione": _denominazione, "codice": _codice,
            "denominazioneBreveAliquotaIva": _denominazioneBreveAliquotaIva,
            "percentualeAliquotaIva": _percentualeAliquotaIva,
            "idUnitaBase": _idUnitaBase,
            "unitaBase": _unitaBase,
            "idGruppoTaglia": _idGruppoTaglia,
            "gruppoTaglia": _gruppoTaglia,
            "idTaglia": _idTaglia,
            "taglia": _taglia,
            "idColore": _idColore,
            "colore": _colore,
            "idAnno": _idAnno,
            "anno": _anno,
            "idStagione": _idStagione,
            "stagione": _stagione,
            "idGenere": _idGenere,
            "genere": _genere}

def leggiListino(idListino, idArticolo=None):
    """
    Restituisce un dizionario con le informazioni sul listino letto
    """
    _denominazione = ''
    _prezzoIngrosso = 0
    _prezzoDettaglio = 0

    if idListino is not None:
        try:
            daoListino = Listino(id=idListino).getRecord()
            if daoListino is not None:
                _denominazione = daoListino.denominazione
        except:
            pass

        try:
            if idArticolo is not None:
                daoListinoArticolo = ListinoArticolo(isList=True).select(idListino=idListino,
                                                                        idArticolo= idArticolo,
                                                                            batchSize=None)
                if "PromoWear" in Environment.modulesList and Environment.taglia_colore:
                        try:
                            articolo = ArticoloTagliaColore(id=idArticolo).getRecord()
                            idArticoloPadre = articolo.id_articolo_padre
                            if idArticoloPadre is not None:
                                try:
                                    daoListinoArticolo = ListinoArticolo(idListino=idListino,
                                                                        idArticolo= idArticoloPadre,
                                                                        batchSize=None)
                                except Exception:
                                    daoListinoArticolo = None
                        except:
                            pass
                if daoListinoArticolo is not None:
                    _prezzoIngrosso = daoListinoArticolo.prezzo_ingrosso
                    _prezzoDettaglio = daoListinoArticolo.prezzo_dettaglio
        except:
            pass

    return {"denominazione": _denominazione,
            "prezzoIngrosso": _prezzoIngrosso,
            "prezzoDettaglio": _prezzoDettaglio}

def fillComboboxMultipli(combobox, idArticolo=None, noSottoMultipli=False, filter=False):
    """
    Crea l'elenco dei multipli
    """

    model = gtk.ListStore(object, int, str, float)
    # multipli legati all'articolo
    muls = Multiplo(isList=True).select(denominazione=None,
                                         idArticolo=idArticolo,
                                         idUnitaBase=None,
                                         orderBy = None,
                                         offset = None,
                                         batchSize = None)
                                        
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow, 0))

    if noSottoMultipli:
        muls = [ item for item in muls if item.moltiplicatore > 1 ]

    for m in muls:
        model.append((m, m.id, m.denominazione, m.moltiplicatore))

    if "PromoWear" in Environment.modulesList and Environment.conf.PromoWear.taglia_colore=="yes":
        try:
            articolo = ArticoloTagliaColore(id=idArticolo).getRecord()
            if articolo.id_articolo_padre is not None:
                # multipli legati all'articolo padre
                muls = Multiplo(isList=True).select(denominazione=None,
                                                     idArticolo=articolo.id_articolo_padre,
                                                     idUnitaBase=None,
                                                     orderBy = None,
                                                     offset = None,
                                                     batchSize = None)

                if noSottoMultipli:
                    muls = [ item for item in muls if item.moltiplicatore > 1 ]

                for m in muls:
                    model.append((m, m.id, '<' + m.denominazione + '>', m.moltiplicatore))
        except:
            pass

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)

def fillComboboxListiniFiltrati(combobox, idArticolo=None, idMagazzino=None, idCliente=None, filter=False):
    """
    Crea l'elenco dei listini
    """
    model = gtk.ListStore(gobject.TYPE_PYOBJECT, int, str)
    liss = Environment.connection.execStoredProcedure('ListinoCandidateSel',
                                                      (None, idArticolo, idMagazzino, idCliente))

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for l in liss:
        model.append((l, l['id'], (l['denominazione'] or '')[0:20]))

    if "PromoWear" in Environment.modulesList and Environment.conf.PromoWear.taglia_colore=="yes":
        try:
            articolo = ArticoloTagliaColore(Environment.connection, idArticolo)
            if articolo is not None:
                if articolo.id_articolo_padre is not None:
                    # listini legati all'articolo padre
                    liss = Environment.connection.execStoredProcedure('ListinoCandidateSel',
                                                                      (None, articolo.id_articolo_padre,
                                                                       idMagazzino, idCliente))

                    for l in liss:
                        model.append((l, l['id'], '<' + (l['denominazione'] or '')[0:20] + '>'))
        except:
            pass

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)

def fillComboboxGruppiTaglia(combobox, filter=False, ignoraVuoti=False,
                             selectedId=None):
    # Crea l'elenco dei gruppi taglia
    selected = None
    model = gtk.ListStore(object, int, str)
    grts = GruppoTaglia(isList=True).select(denominazione=None,
                                             orderBy = None,
                                             offset = None,
                                             batchSize = None)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    currIdx = 0
    for i, g in enumerate(grts):
        if ignoraVuoti and len(g.taglie) == 0:
            continue
        currIdx += 1
        model.append((g, g.id, (g.denominazione or '')[0:25]))
        if g.id == selectedId:
            selected = currIdx

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)

    if selected is not None:
        combobox.set_active(selected)


def fillComboboxTaglie(combobox, filter=False, idGruppoTaglia=None, ignore=[]):
    # Crea l'elenco delle taglie, ignorando quelle presenti nella lista ignore

    model = gtk.ListStore(object, int, str)
    if idGruppoTaglia is None:
        tags = Taglia(isList=True).select(denominazione=None,
                                           orderBy = None,
                                           offset = None,
                                           batchSize = None)

        if not filter:
            emptyRow = ''
        else:
            emptyRow = '< Tutti >'
        model.append((None, 0, emptyRow))
        for t in tags:
            if ignore and t.id in ignore:
                continue
            model.append((t, t.id, (t.denominazione or '')[0:25]))
    else:
        tags = GruppoTagliaTaglia(isList=True).select( idGruppoTaglia=idGruppoTaglia,
                                                       orderBy = None,
                                                       offset = None,
                                                       batchSize = None)
        if not filter:
            emptyRow = ''
        else:
            emptyRow = '< Tutti >'
        model.append((None, 0, emptyRow))
        for t in tags:
            if ignore and t.id_taglia in ignore:
                continue
            model.append((t, t.id_taglia, (t.denominazione_taglia or '')[0:25]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)


def fillComboboxColori(combobox, filter=False, ignore=[]):
    # Crea l'elenco dei colori, ignorando quelli presenti nella lista ignore

    model = gtk.ListStore(gobject.TYPE_PYOBJECT, int, str)
    cols = Colore(isList=True).select( denominazione=None,
                                       orderBy = None,
                                       offset = None,
                                       batchSize = None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for c in cols:
        if ignore and c.id in ignore:
            continue
        model.append((c, c.id, (c.denominazione or '')[0:25]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)


def fillComboboxAnniAbbigliamento(combobox, filter=False):
    #crea l'elenco degli anni per l'abbigliamento
    #queryString = ('SELECT * FROM promogest.anno_abbigliamento')
    #argList = []
    #Environment.connection._cursor.execute(queryString, argList)
    #res = Environment.connection._cursor.fetchall()
    res = AnnoAbbigliamento(isList=True).select()
    model = gtk.ListStore(object, int, str)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for a in res:
        model.append((a, a.id, a.denominazione))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)


def fillComboboxStagioniAbbigliamento(combobox, filter=False):
    #crea l'elenco degli anni per l'abbigliamento
    #queryString = ('SELECT * FROM promogest.stagione_abbigliamento')
    #argList = []
    #Environment.connection._cursor.execute(queryString, argList)
    #res = Environment.connection._cursor.fetchall()
    res = StagioneAbbigliamento(isList=True).select(batchSize=None)
    model = gtk.ListStore(object, int, str)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for s in res:
        model.append((s, s.id, s.denominazione))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)


def fillComboboxGeneriAbbigliamento(combobox, filter=False):
    #crea l'elenco degli anni per l'abbigliamento
    #queryString = ('SELECT * FROM promogest.genere_abbigliamento')
    #argList = []
    #Environment.connection._cursor.execute(queryString, argList)
    #res = Environment.connection._cursor.fetchall()
    res = GenereAbbigliamento(isList=True).select(batchSize=None)
    model = gtk.ListStore(object, int, str)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for g in res:
        model.append((g, g.id, g.denominazione))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)

def on_id_gruppo_taglia_customcombobox_clicked(widget, button):
    #richiama l'anagrafica dei gruppi taglia

    def on_anagrafica_gruppi_taglia_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxGruppiTaglia(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaGruppiTaglia import AnagraficaGruppiTaglia
    anag = AnagraficaGruppiTaglia()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_gruppi_taglia_destroyed)


def on_id_taglia_customcombobox_clicked(widget, button, idGruppoTaglia=None, ignore=None):
    #richiama l'anagrafica delle taglie

    def on_anagrafica_taglie_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxTaglie(widget.combobox, idGruppoTaglia=idGruppoTaglia, ignore=ignore)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaTaglie import AnagraficaTaglie
    anag = AnagraficaTaglie()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_taglie_destroyed)


def on_id_colore_customcombobox_clicked(widget, button, ignore=None):
    #richiama l'anagrafica dei colori

    def on_anagrafica_colori_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxColori(widget.combobox, ignore=ignore)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaColori import AnagraficaColori
    anag = AnagraficaColori()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_colori_destroyed)
