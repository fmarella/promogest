# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>


from promogest.dao.UnitaBase import UnitaBase
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.Articolo import Articolo
from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
from promogest.modules.PromoWear.dao.GruppoTagliaTaglia import GruppoTagliaTaglia
from promogest.modules.PromoWear.dao.Taglia import Taglia
from promogest.modules.PromoWear.dao.Colore import Colore
from promogest.modules.PromoWear.dao.Modello import Modello
from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento
import promogest.dao.Listino
from promogest.ui.utils import findIdFromCombobox, findComboboxRowFromId, posso
from promogest import Environment
import gtk
import gobject


def leggiFornituraPromoWear(idArticolo, idFornitore=None, data=None, noPreferenziale=False):
    """ Restituisce un dizionario con le informazioni sulla fornitura letta """
    from promogest.dao.Fornitura import Fornitura
    from promogest.dao.ScontoFornitura import ScontoFornitura
    _prezzoLordo = 0
    _prezzoNetto = 0
    _sconti = []
    _applicazioneSconti = 'scalare'
    _codiceArticoloFornitore = ''

    if (idArticolo is not None):
        fors = Fornitura().select(idArticolo=idArticolo,
                                    idFornitore=None,
                                    daDataFornitura=None,
                                    aDataFornitura=None,
                                    daDataPrezzo=None,
                                    aDataPrezzo=data,
                                    codiceArticoloFornitore=None,
                                    orderBy = 'data_prezzo DESC, fornitore_preferenziale DESC',
                                    offset = None,
                                    batchSize = None)

        fornitura = None
        if idFornitore is not None:
            # cerca tra tutti i fornitori quello utile, o in sua assenza, quello preferenziale
            for f in fors:
                if f.id_fornitore == idFornitore:
                    fornitura = f
                    break
                elif not(noPreferenziale) and f.fornitore_preferenziale:
                    fornitura = f
        else:
            if len(fors) > 0:
                fornitura = fors[0]

        if fornitura is not None:
            _codiceArticoloFornitore = fornitura.codice_articolo_fornitore or ''
            _prezzoLordo = fornitura.prezzo_lordo or 0
            _prezzoNetto = _prezzoLordo
            _applicazioneSconti = fornitura.applicazione_sconti

            idFornitura = fornitura.id
            if idFornitura is not None:
                scos = ScontoFornitura().select(idFornitura=idFornitura)

                for s in scos:
                    _sconti.append({"valore": s.valore, "tipo": s.tipo_sconto})

                    if s.tipo_sconto == 'percentuale':
                        if _applicazioneSconti == 'scalare':
                            _prezzoNetto = float(_prezzoNetto) * (1 - float(s.valore) / 100)
                        elif _applicazioneSconti == 'non scalare':
                            _prezzoNetto = float(_prezzoNetto) - float(_prezzoLordo) * float(s.valore) / 100
                    elif s.tipo_sconto == 'valore':
                        _prezzoNetto = float(_prezzoNetto) - float(s.valore)
    return {"prezzoLordo": _prezzoLordo,
            "prezzoNetto": _prezzoNetto,
            "sconti": _sconti,
            "applicazioneSconti": _applicazioneSconti,
            "codiceArticoloFornitore": _codiceArticoloFornitore}




def leggiArticoloPromoWear(id, full=False):
    # restituisce un dizionario con le informazioni sull'articolo letto
    articleDict = {}
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
    _ordine = 1
    _taglia = ''
    _idColore = None
    _colore = ''
    _idAnno = None
    _anno = ''
    _idStagione = None
    _stagione = ''
    _idGenere = None
    _genere = ''

    def numero_ordine(_idTaglia, _idGruppoTaglia):
        if _idGruppoTaglia and _idTaglia:
            gtt = GruppoTagliaTaglia().select(idGruppoTaglia = _idGruppoTaglia,
                                                    idTaglia= _idTaglia)
            if gtt:
                return gtt[0].ordine
            else:
                return 1

    if id is not None:
        daoArticolo = Articolo().getRecord(id=id)
        if daoArticolo is not None:
            _id = id
            _denominazione = daoArticolo.denominazione or ''
            _codice = daoArticolo.codice or ''
            _idUnitaBase = daoArticolo.id_unita_base
            if _idUnitaBase is not None:
                res = UnitaBase().select(batchSize=None)
                if res is not None:
                    _unitaBase = res[0].denominazione
            if daoArticolo.id_aliquota_iva is not None:
                daoAliquotaIva = AliquotaIva().getRecord(id=daoArticolo.id_aliquota_iva)
                if daoAliquotaIva is not None:
                    _denominazioneBreveAliquotaIva = daoAliquotaIva.denominazione_breve or ''
                    _percentualeAliquotaIva = daoAliquotaIva.percentuale or 0
            if posso("PW"):
                daoArticoloTagliaColore = daoArticolo
                if daoArticoloTagliaColore is not None:
                    _idGruppoTaglia = daoArticoloTagliaColore.id_gruppo_taglia
                    _gruppoTaglia = daoArticoloTagliaColore.denominazione_gruppo_taglia or '-'
                    _idTaglia = daoArticoloTagliaColore.id_taglia
                    _taglia = daoArticoloTagliaColore.denominazione_taglia or '-'
                    _idColore = daoArticoloTagliaColore.id_colore
                    _colore = daoArticoloTagliaColore.denominazione_colore or '-'
                    _ordine = numero_ordine(_idTaglia, _idGruppoTaglia)
                    _idAnno = daoArticoloTagliaColore.id_anno
                    _anno = daoArticoloTagliaColore.anno or '-'
                    _idStagione = daoArticoloTagliaColore.id_stagione
                    _stagione = daoArticoloTagliaColore.stagione or '-'
                    _idGenere = daoArticoloTagliaColore.id_genere
                    _genere = daoArticoloTagliaColore.genere or '-'
        articleDict= {"id": _id,
                    "denominazione": _denominazione, "codice": _codice,
                    "denominazioneBreveAliquotaIva": _denominazioneBreveAliquotaIva,
                    "percentualeAliquotaIva": _percentualeAliquotaIva,
                    "idUnitaBase": _idUnitaBase,
                    "unitaBase": _unitaBase,
                    "idGruppoTaglia": _idGruppoTaglia,
                    "gruppoTaglia": _gruppoTaglia,
                    "idTaglia": _idTaglia,
                    "ordine":_ordine,
                    "taglia": _taglia,
                    "idColore": _idColore,
                    "colore": _colore,
                    "idAnno": _idAnno,
                    "anno": _anno,
                    "idStagione": _idStagione,
                    "stagione": _stagione,
                    "idGenere": _idGenere,
                    "genere": _genere,
                    "daoArticolo":daoArticolo}
    return articleDict

def leggiListino(idListino, idArticolo=None):
    """
    Restituisce un dizionario con le informazioni sul listino letto
    """
    _denominazione = ''
    _prezzoIngrosso = 0
    _prezzoDettaglio = 0

    if idListino is not None:
        try:
            daoListino = Listino().getRecord(id=idListino)
            if daoListino is not None:
                _denominazione = daoListino.denominazione
        except:
            pass

        try:
            if idArticolo is not None:
                daoListinoArticolo = ListinoArticolo().select(idListino=idListino,
                                                                idArticolo= idArticolo,
                                                                batchSize=None)
                if posso("PW"):
                        try:
                            articolo = ArticoloTagliaColore().getRecord(id=idArticolo)
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
    muls = Multiplo().select(denominazione=None,
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

    if posso("PW"):
        try:
            articolo = ArticoloTagliaColore().getRecord(id=idArticolo)
            if articolo.id_articolo_padre is not None:
                # multipli legati all'articolo padre
                muls = Multiplo().select(denominazione=None,
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

    if posso("PW") and Environment.conf.PromoWear.taglia_colore=="yes":
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
    grts = GruppoTaglia().select(denominazione=None,
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
        tags = Taglia().select(denominazione=None,
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
        tags = GruppoTagliaTaglia().select( idGruppoTaglia=idGruppoTaglia,
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
    cols = Colore().select( denominazione=None,
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

def fillComboboxModelli(combobox, filter=False, ignore=[]):
    # Crea l'elenco dei modelli, ignorando quelli presenti nella lista ignore

    model = gtk.ListStore(object, int, str)
    cols = Modello().select( denominazione=None,
                                       orderBy = None,
                                       offset = None,
                                       batchSize = None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for c in cols:
        model.append((c, c.id, (c.denominazione or '')[0:25]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)

def fillComboboxAnniAbbigliamento(combobox, filter=False):
    #crea l'elenco degli anni per l'abbigliamento
    res = AnnoAbbigliamento().select()
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
    res = StagioneAbbigliamento().select(batchSize=None)
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
    res = GenereAbbigliamento().select(batchSize=None)
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

def on_id_modello_customcombobox_clicked(widget, button):
    #richiama l'anagrafica dei modelli

    def on_anagrafica_modello_destroyed(window):
        # all'uscita dall'anagrafica richiamata, aggiorna l'elenco associato
        widget.button.set_active(False)
        id = findIdFromCombobox(widget.combobox)
        fillComboboxModelli(widget.combobox)
        findComboboxRowFromId(widget.combobox, id)


    if widget.button.get_property('active') is False:
        return

    from AnagraficaModelli import AnagraficaModelli
    anag = AnagraficaModelli()

    anagWindow = anag.getTopLevel()
    returnWindow = widget.get_toplevel()
    anagWindow.set_transient_for(returnWindow)
    anagWindow.show_all()
    anagWindow.connect("destroy",
                        on_anagrafica_modello_destroyed)


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
    anagWindow.connect("destroy", on_anagrafica_taglie_destroyed)


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
