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

import gobject, os, decimal
from decimal import *
import pygtk
pygtk.require('2.0')
import gtk
import time, datetime
from promogest import Environment

from sqlalchemy.orm import *
from sqlalchemy import *
#from utils import leggiAgente
import string, re
import xml.etree.cElementTree as ElementTree
from xml.etree.cElementTree import *

# Letture per recuperare velocemente dati da uno o piu' dao correlati

# Riempimento lookup combobox


def fillComboboxAliquoteIva(combobox, filter=False):
    """
    Crea l'elenco delle aliquote iva
    """
    from promogest.dao.AliquotaIva import AliquotaIva
    model = gtk.ListStore(object, int, str)
    ivas = AliquotaIva().select(offset=None,batchSize=None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for i in ivas:
        model.append((i, i.id, i.denominazione))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)


def fillComboboxTipiAliquoteIva(combobox, filter=False):
    """
    Crea l'elenco dei tipi aliquota iva
    """
    from promogest.dao.TipoAliquotaIva import TipoAliquotaIva
    res = TipoAliquotaIva().select(offset=None,batchSize=None)
    model = gtk.ListStore(object, int, str)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for t in res:
        model.append([t, t.id, t.denominazione])

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxCategorieArticoli(combobox, filter=False):
    """
    Crea l'elenco delle categorie articoli
    """
    from promogest.dao.CategoriaArticolo import CategoriaArticolo
    model = gtk.ListStore(object, int, str)
    cats = CategoriaArticolo().select(offset=None,batchSize=None, orderBy=CategoriaArticolo.denominazione)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for c in cats:

        model.append((c, c.id, (c.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxCCardType(combobox, filter=False):
    """
    Crea l'elenco dei tipi di carte di credito
    """
    from promogest.dao.CCardType import CCardType
    model = gtk.ListStore(object, int, str)
    cats = CCardType().select(offset=None,batchSize=None, orderBy=CCardType.denominazione)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for c in cats:

        model.append((c, c.id, (c.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxFamiglieArticoli(combobox, filter=False, ignore=[]):
    """
    Crea l'elenco delle famiglie articoli
    """
    from promogest.dao.FamigliaArticolo import FamigliaArticolo
    model = gtk.TreeStore(object, int, str)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append(None, (None, 0, emptyRow))

    def recurse(padre,f):
        for s in f.children:
            figlio1 = model.append(padre, (s,
                                (s.id ),
                                (s.denominazione or ''),
                                ))
            recurse(figlio1,s)
    for f in FamigliaArticolo().select(batchSize=None):
        if not f.parent:
            padre = model.append(None, (f,
                                (f.id ),
                                (f.denominazione or ''),
                                ))
            if f.children:
                recurse(padre,f)

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxImballaggi(combobox, filter=False):
    """
    Crea l'elenco degli imballaggi
    """
    from promogest.dao.Imballaggio import Imballaggio
    model = gtk.ListStore(object, int, str)
    imbs = Imballaggio().select(offset=None,batchSize=None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for i in imbs:
        model.append((i, i.id, (i.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxStatiArticoli(combobox, filter=False):
    """ Crea l'elenco degli stati articoli """
    from promogest.dao.StatoArticolo import StatoArticolo
    model = gtk.ListStore(object, int, str)
    stas = StatoArticolo().select(offset=None,batchSize=None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for s in stas:
        model.append((s, s.id, (s.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxUnitaBase(combobox, filter=False):
    """ Crea l'elenco delle unita base """
    from promogest.dao.UnitaBase import UnitaBase
    res = UnitaBase().select(offset=None,batchSize=None)
    model = gtk.ListStore(object, int, str)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for u in res:
        model.append((u, u.id, u.denominazione or '')[0:20])

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxRole(combobox, filter=False):
    """
    Crea l'elenco dei ruoli
    """
    from promogest.modules.RuoliAzioni.dao.Role import Role
    res = Role().select(offset=None,batchSize=None)
    model = gtk.ListStore(object, int, str)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for u in res:
        model.append((u, u.id, u.name or '')[0:20])

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxLang(combobox, filter=False):
    """
    Crea l'elenco delle lingue
    """
    from promogest.modules.Multilingua.dao.Language import Language
    res = Language().select(offset=None,batchSize=None)
    model = gtk.ListStore(object, int, str)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for u in res:
        model.append((u, u.id, u.denominazione or '')[0:20])

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)


def fillComboboxUnitaFisica(combobox, tipo):
    """
    Crea l'elenco per le unita di peso, lunghezza, volume usate
    """
    from promogest.dao.UnitaBase import UnitaBase
    #unitaFisica = 'unita_' + tipo
    model = gtk.ListStore(str)
    res = UnitaBase().select(offset=None,batchSize=None)
    for u in res:
        #unita = (u[unitaFisica] or '')[0:20]
        unita = (u.denominazione or '')[0:20]
        if unita is not '':
            model.append((unita, ))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 0)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(0)


def fillComboboxCategorieClienti(combobox, filter=False):
    """
    Crea l'elenco delle categorie clienti
    """
    from  promogest.dao.CategoriaCliente import CategoriaCliente
    model = gtk.ListStore(object, int, str)
    cats = CategoriaCliente().select(offset=None,batchSize=None)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for c in cats:
        model.append((c, c.id, (c.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxCategorieContatti(combobox, filter=False):
    """
    Crea l'elenco delle categorie contatti
    """
    from promogest.dao.CategoriaContatto import CategoriaContatto
    model = gtk.ListStore(object, int, str)
    cats = CategoriaContatto().select(offset=None,batchSize=None)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for c in cats:
        model.append((c, c.id, (c.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxCategorieFornitori(combobox, filter=False):
    """
    Crea l'elenco delle categorie fornitori
    """
    from promogest.dao.CategoriaFornitore import CategoriaFornitore
    model = gtk.ListStore(gobject.TYPE_PYOBJECT, int, str)
    cats = CategoriaFornitore().select(offset=None,batchSize=None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for c in cats:
        model.append((c, c.id, (c.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)


def fillComboboxMultipli(combobox, idArticolo=None, noSottoMultipli=False, filter=False):
    """
    Crea l'elenco dei multipli
    """
    from promogest.dao.Multiplo import Multiplo
    model = gtk.ListStore(object, int, str, float)
    # multipli legati all'articolo
    muls = Multiplo().select(offset=None,batchSize=None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow, 0))

    if noSottoMultipli:
        muls = [ item for item in muls if item.moltiplicatore > 1 ]

    for m in muls:
        model.append((m, m.id, m.denominazione_breve, m.moltiplicatore))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)


def fillComboboxListini(combobox, filter=False):
    """
    Crea l'elenco dei listini
    """
    from promogest.dao.Listino import Listino
    model = gtk.ListStore(object, int, str)
    liss= Listino().select(denominazione=None,offset=None,orderBy = None,batchSize=None)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for l in liss:
        model.append((l, l.id, (l.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxListiniComplessi(combobox,idListinoComplesso=None, filter=False):
    """
    Crea l'elenco dei listini
    """
    from promogest.dao.ListinoComplessoListino import ListinoComplessoListino
    model = gtk.ListStore(object, int, str)
    liss= ListinoComplessoListino().select(idListinoComplesso=idListinoComplesso,offset=None,batchSize=None)

    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for l in liss:
        model.append((l, l.id_listino, (l.listino_denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)


def listinoCandidateSel(OrderBy=None,idArticolo=None,idMagazzino=None,idCliente=None):
    from promogest.dao.Listino import Listino
    from promogest.dao.ListinoMagazzino import ListinoMagazzino
    from promogest.dao.ListinoArticolo import ListinoArticolo
    from promogest.dao.ListinoCategoriaCliente import ListinoCategoriaCliente
    from promogest.dao.ClienteCategoriaCliente import ClienteCategoriaCliente

    def _dirtyWork(OrderBy=None,idArticolo=None,idMagazzino=None,idCliente=None):
        if idArticolo:
            filter1 = Listino.id.in_(select([ListinoArticolo.id_listino], ListinoArticolo.id_articolo == idArticolo))
        else:
            filter1 = None

        if idMagazzino:
            filter2 = or_(Listino.id.in_(select([ListinoMagazzino.id_listino], ListinoMagazzino.id_magazzino == idMagazzino)),
                        not_(Listino.id.in_(select([ListinoMagazzino.id_listino]).distinct())))
        else :
            filter2 = None

        if idCliente:
            filter3 = or_(Listino.id.in_(select([ListinoCategoriaCliente.id_listino] ,
                            ListinoCategoriaCliente.id_categoria_cliente.in_(select([ClienteCategoriaCliente.id_categoria_cliente] ,
                                ClienteCategoriaCliente.id_cliente ==idCliente)))),
                            not_(Listino.id.in_(select([ListinoCategoriaCliente.id_listino]).distinct())))
        else :
            filter3 = None

        filter4 = and_(Listino.listino_attuale == True)

        if not OrderBy:
            OrderBy= "denominazione"

        listinoSelezionato = Listino().select(complexFilter=and_(filter1,filter2,filter3, filter4), orderBy=OrderBy)
        return listinoSelezionato
    listin = _dirtyWork(OrderBy=OrderBy,idArticolo=idArticolo,
                                    idMagazzino=idMagazzino,idCliente=idCliente)
    if not listin and "PromoWear" in Environment.modulesList:
        from promogest.dao.Articolo import Articolo
        father = Articolo().getRecord(id=idArticolo)
        idArticolo = father.id_articolo_padre
        listinPadre = _dirtyWork(OrderBy=OrderBy,idArticolo=idArticolo,
                                    idMagazzino=idMagazzino,idCliente=idCliente)
        if listinPadre:
            listin = listinPadre
            print "LISTINO ASSOCIATO AL PADRE IN QUANDO FIGLIO NON NE AVEVA UNO", listin
            return listin
    else:
        Environment.pg2log.info("LISTINI ASSOCIATI: "+str(listin))
        return listin

def fillComboboxListiniFiltrati(combobox, idArticolo=None, idMagazzino=None, idCliente=None, filter=False):
    """
    Crea l'elenco dei listini
    """
    model = gtk.ListStore(object, int, str)
    liss = listinoCandidateSel( idArticolo=idArticolo, idMagazzino=idMagazzino, idCliente = idCliente)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    if liss:
        for l in liss:
            model.append((l, l.id, (l.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    #if combobox.__class__ is gtk.ComboBoxEntry:
        #combobox.set_text_column(2)

def fillComboboxFornitori(combobox,filter=False, noempty=False):
    """ Crea l'elenco dei fornitori in una combo """
    from promogest.dao.Fornitore import Fornitore
    model = gtk.ListStore(gobject.TYPE_PYOBJECT, int, str)
    forns = Fornitore().select(offset=None,batchSize=None)
    if not noempty:
        if not filter:
            emptyRow = ''
        else:
            empyRow = '<Tutti>'
        model.append((None, 0, emptyRow))
    for f in forns:
        model.append((f, f.id, (f.ragione_sociale or '')[:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxMagazzini(combobox, filter=False, noempty=False):
    """  Crea l'elenco dei magazzini  """
    from promogest.dao.Magazzino import Magazzino
    model = gtk.ListStore(object, int, str)
    mags = Magazzino().select(offset=None,batchSize=None)
    if not noempty:
        if not filter:
            emptyRow = ''
        else:
            emptyRow = '< Tutti >'
        model.append((None, 0, emptyRow))
    for m in mags:
        model.append((m, m.id, (m.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxOperazioni(combobox, tipo=None, filter=False):
    """
    Crea l'elenco delle operazioni per la movimentazione di magazzino """
    from promogest.dao.Operazione import Operazione
    if tipo:
#        res = Environment.params['session'].query(Operazione).filter(Operazione.tipo_operazione==tipo).order_by(Operazione.denominazione).all()
        res = Environment.params['session'].query(Operazione).filter(or_(Operazione.tipo_operazione==None,Operazione.tipo_operazione==tipo)).order_by(Operazione.denominazione).all()
    else:
        res = Environment.params['session'].query(Operazione).filter(Operazione.tipo_operazione==None).order_by(Operazione.denominazione).all()
    model = gtk.ListStore(object, str, str)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, '', emptyRow))
    for o in res:
        model.append((o, o.denominazione, (o.denominazione or '')[0:30]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)


def fillComboboxTipiRecapito(combobox):
    """ Crea l'elenco dei tipi di recapito per i contatti """
    model = fillModelTipiRecapito()

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 0)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(0)

def fillModelTipiRecapito():
    """ Crea l'elenco dei tipi di recapito per i contatti  """
    from promogest.dao.TipoRecapito import TipoRecapito
    res = TipoRecapito().select(orderBy=TipoRecapito.denominazione)
    model = gtk.ListStore(str)
    model.append(('', ))
    for r in res:
        model.append((r.denominazione, ))
    return model

def fillComboboxAziende(combobox, filter=False):
    """ Crea l'elenco delle aziende  """
    from promogest.dao.Azienda import Azienda
    model = gtk.ListStore(object, str, str)
    res = Azienda().select(offset=None,batchSize=None, orderBy=Azienda.schemaa)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, None, emptyRow))
    for a in res:
        model.append((a, a.schemaa, (a.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxPagamenti(combobox, filter=False):
    """ Crea l'elenco dei pagamenti  """
    from promogest.dao.Pagamento import Pagamento
    model = gtk.ListStore(object, int, str)
    pags = Pagamento().select(offset=None,batchSize=None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for p in pags:
        model.append((p, p.id, (p.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def getModelsName():
    """Scans all xml files in models directory.

    It returns a dictionary containing models' names and relatives paths"""
    modelsDir = Environment.documentsDir + 'modelli_listini'
    if not (os.path.exists(modelsDir)):
        os.mkdir(modelsDir)
    file_list = os.listdir(modelsDir)
    existingModels = {}
    for file in file_list:
        if file[-3:].upper() == 'PGX':
            path = modelsDir + os.sep + file
        if os.path.isfile(path):
            f = open(path, 'r')
            tree = parse(f)
            model_tag = tree.getroot()
            if model_tag.tag == 'model':
                existingModels[model_tag.attrib['name']] = path
    return existingModels

def fillModelCombobox(combobox):
    """Appends in combobox tuples containing,
    for each file in models directory, model's name and its path"""
    existingModels = getModelsName()
    model = gtk.ListStore(str,str)
    model.append((None,None))
    if existingModels:
        for (m,p) in existingModels.iteritems():
            model.append((m,p))
    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 0)
    combobox.set_model(model)

def fillComboboxBanche(combobox, filter=False):
    """
    Crea elenco delle banche
    """
    from promogest.dao.Banca import Banca
    model = gtk.ListStore(object, int, str)
    bans = Banca().select(offset=None,batchSize=None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for b in bans:
        model.append((b, b.id, (b.denominazione  or '')))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxCausaliTrasporto(combobox, filter=False):
    """ Crea elenco delle causali di trasporto  """
    from promogest.dao.TestataDocumento import TestataDocumento
    res = Environment.params['session'].query(TestataDocumento.causale_trasporto).distinct()
    model = gtk.ListStore(object, str)
    #res = []
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, emptyRow))
    for t in res:
        model.append((t, (t.causale_trasporto or '')[0:30]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 1)
    combobox.set_model(model)
    print "MODEL", len(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(1)

def fillComboboxAspettoEsterioreBeni(combobox, filter=False):
    """ Crea elenco degli aspetti esteriori beni """
    from promogest.dao.TestataDocumento import TestataDocumento
    #res = TestataDocumento().select(batchSize=None, offset=None,orderBy='aspetto_esteriore_beni')
    #queryString = ('SELECT DISTINCT aspetto_esteriore_beni FROM ' + Environment.connection._schemaAzienda + '.testata_documento ORDER BY aspetto_esteriore_beni')
    #argList = []
    #Environment.connection._cursor.execute(queryString, argList)
    #res = Environment.connection._cursor.fetchall()
    res = Environment.params['session'].query(TestataDocumento.aspetto_esteriore_beni).distinct()
    model = gtk.ListStore(object, str)
    #res = []
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, emptyRow))
    for t in res:
        model.append((t, (t.aspetto_esteriore_beni or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 1)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(1)

def fillComboboxPortoTrasporto(combobox):
    """ Crea l'elenco dei porti trasporto """
    model = gtk.ListStore(gobject.TYPE_STRING)
    model.append(('Franco'))
    model.append(('Assegnato'))
    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 1)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(1)

def fillComboboxDestinazioniMerce(combobox, idCliente=None, filter=False):
    """ Crea l'elenco delle destinazioni merce """
    from promogest.dao.DestinazioneMerce import DestinazioneMerce
    model = gtk.ListStore(object, int, str)
    dems = DestinazioneMerce().select(idCliente=idCliente, batchSize=None,offset=None )
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow))
    for d in dems:
        model.append((d, d.id, (d.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxAutoriPromemoria(combobox):
    """ Crea l'elenco degli autori gia'inseriti """
    from promogest.dao.Promemoria import Promemoria
    #autors = Promemoria().select(orderBy="autore")
    res = Environment.params['session'].query(Promemoria.autore).distinct()
    model = gtk.ListStore(str)
    for c in res:
        model.append([c.autore])
    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 0)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(0)

def fillComboboxNotePiePaginaTestataDocumento(combobox):
    """ Crea l'elenco degli autori gia'inseriti """
    from promogest.dao.TestataDocumento import TestataDocumento
    #autors = Promemoria().select(orderBy="autore")
    res = Environment.params['session'].query(TestataDocumento.note_pie_pagina).distinct()
    model = gtk.ListStore(str)
    for c in res:
        if c.note_pie_pagina:
            if "Rif. DDT" not in c.note_pie_pagina:
                model.append([c.note_pie_pagina])
    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 0)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(0)



def fillComboboxIncaricatiPromemoria(combobox):
    """
    Crea l'elenco degli incaricati gia'inseriti
    """
    from promogest.dao.Promemoria import Promemoria
    #argList = []
    model = gtk.ListStore(str)
    #autors = Promemoria().select(orderBy="incaricato")
    res = Environment.params['session'].query(Promemoria.incaricato).distinct()
    #for a in autors:
        #argList.append(a.incaricato)
    #b = list(set(argList))
    for  c in res:
        model.append([c.incaricato])

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 0)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(0)


# Operazioni su lookup combobox

def findComboboxRowFromId(combobox, id):
    """
    evidenzia la riga di una combobox relativa ad un id
    """

    def findTreeStoreRow(model, path, iter, (combobox, id)):
        """
        evidenzia la riga di una combobox relativa ad un id in un albero
        """

        r = model.get_value(iter, 1)
        if r == id:
            combobox.set_active_iter(iter)
            return True

    def findListStoreRow(model, combobox, id):
        """
        evidenzia la riga di una combobox relativa ad un id in una lista
        """

        for r in model:
            if r[1] == id:
                combobox.set_active_iter(r.iter)

    combobox.set_active(-1)
    if not(id is None or id == 0):
        model = combobox.get_model()

        if model.__class__ is gtk.TreeStore:
            model.foreach(findTreeStoreRow, (combobox, id))
        elif model.__class__ is gtk.ListStore:
            findListStoreRow(model, combobox, id)


def findComboboxRowFromStr(combobox, string, column):
    """
    evidenzia la riga di una combobox relativa ad una descrizione
    """

    combobox.set_active(-1)
    if not(string is None or string == ''):
        model = combobox.get_model()
        for r in model:
            if r[column] == string:
                combobox.set_active_iter(r.iter)


def findIdFromCombobox(combobox):
    """
    Restituisce l' id relativo alla riga selezionata in un elenco a discesa
    """

    model = combobox.get_model()
    iterator = combobox.get_active_iter()
    if iterator is not None:
        id = model.get_value(iterator, 1)
        if id == 0:
            return None
        else:
            return id
    else:
        return None


def findStrFromCombobox(combobox, column):
    """
    Restituisce la stringa relativa alla riga selezionata in un elenco a discesa
    """

    model = combobox.get_model()
    iterator = combobox.get_active_iter()
    if iterator is not None:
        return model.get_value(iterator, column)
    else:
        return ''

def on_combobox_articolo_search_clicked(combobox, callName=None):
    """
    richiama la ricerca degli articoli
    """

    def refresh_combobox_articolo(anagWindow):
        if anag.dao is None:
            id = None
        else:
            id = anag.dao.id
        res = leggiArticolo(id)
        combobox.refresh(id, res["denominazione"], res)
        anagWindow.destroy()
        if callName is not None:
            callName()


    if combobox.on_selection_changed():
        from RicercaArticoli import RicercaArticoli
        anag = RicercaArticoli()

        anagWindow = anag.getTopLevel()
        returnWindow = combobox.get_toplevel()
        anagWindow.set_transient_for(returnWindow)
        anagWindow.show_all()

        anagWindow.connect("hide",
                           refresh_combobox_articolo)
    elif callName is not None:
        callName()


# ---

def setFileName(filename, ext, returnName = False):
    """Verify that the filename have the extension "ext"

    If not, it will append the extension to the end of the filename."""
    name = os.path.split(filename)
    _filename = os.path.splitext(name[1])
    _ext = _filename[1].upper()[1:]

    if _ext == ext.upper():
        if returnName:
            return name[1]
        else:
            return filename

    else:
        if returnName:
            return _filename[0]+'.'+ext.lower()
        else:
            _name = name[0]+os.path.sep+_filename[0]+'.'+ext.lower()
            return _name

def on_typeComboBox_changed(combobox, dialogWidget, currentName, isEvent=True):
    cb_model = combobox.get_model()
    iter = combobox.get_active_iter()
    filters = dialogWidget.list_filters()
    if iter is not None:
        value = cb_model.get_value(iter, 0)
        file_string = dialogWidget.get_filename() or currentName
        if file_string[-3:].upper() == value:
            return (value, file_string)
        elif isEvent:
            if value == 'XML':
                _file_name = str(setFileName(file_string, 'xml', True))
                dialogWidget.set_filter(filters[1])
            elif value == 'CSV':
                _file_name = str(setFileName(file_string, 'csv', True))
                dialogWidget.set_filter(filters[2])
            dialogWidget.set_current_name(_file_name)

        else:
            _file_name = str(setFileName(file_string, value))
            return (value, _file_name)


def fillComboBoxNazione(combobox,default=None):
    """
    nazione
    """
    nationList=["Afganistan","Albania","Algeria","Arabia Saudita","Argentina","Australia",
                "Austria","Belgio","Bermude","Bielorussia","Bolivia","Bosnia-Erzegovina","Brasile",
                "Bulgaria","Canada","Ceca (Repubblica)","Cile","Cina","Cipro","Colombia","Corea del Sud",
                "Costarica","Croazia","Cuba","Danimarca","Egitto","Estonia","Filippine","Finlandia",
                "Francia","Georgia","Germania","Giappone","Gran Bretagna","Grecia","Hong Kong","India",
                "Indonesia","Iran","Iraq","Irlanda","Islanda","Israele","Italia","Kazakstan","Kuwait","Lettonia",
                "Libano","Libia","Lituania","Lussemburgo","Malta","Marocco","Messico","Monaco","Montenegro",
                "Norvegia","Nuova Zelanda","Paesi Bassi", "Perù","Polonia","Portogallo","Regno Unito","Romania",
                "Russia (Federazione)","S.Marino","Senegal","Serbia (Repubblica)","Siria","Slovacca (Repubblica)",
                "Slovenia","Somalia","Spagna","Stati Uniti d'America","Sudafrica","Svezia","Svizzera","Tailandia",
                "Taiwan","Tunisia","Turchia","Ucraina","Ungheria","Unione Europea","Uruguay","Vaticano","Venezuela",
                "Vietnam"]
    model = gtk.ListStore(str)
    if not default:
        emptyRow = 'Italia'
    else:
        emptyRow = 'Italia'
    model.append((emptyRow,))
    for d in nationList:
        model.append([d])
    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 0)
    combobox.set_wrap_width(5)
    combobox.set_active(11)
    combobox.set_model(model)

# cescoap - utility all'autocompletamento delle entry
def autocompletamento_entry(par_entry=None, filtro=None):
    '''Funzione di autocompletamento delle entry'''
    # preleva articoli filtrati dal Dao Articolo
    completion = gtk.EntryCompletion()
    liststore = gtk.ListStore(str, object)
    liststore.append()
    completion.set_model(liststore)
    par_entry.set_completion(completion)
    completion.set_text_column(0)
    # connetto entry all'evento di rilascio del tasto
    par_entry.add_events(gtk.gdk.KEY_RELEASE_MASK)
    par_entry.connect('key-release-event', gestione_testo, filtro)

# cescoap - funzione supplemento a autocompletamento_entry
def gestione_testo(gest_entry, event, filtro):
    ''' Gestione riempimento liststore su base del numero di elementi'''
    from promogest.dao.Articolo import Articolo
    print "Gli argomenti saranno filtrati per: " + filtro
    print "Insert: " + gest_entry.get_text()
    gest_completion = gest_entry.get_completion()
    gest_liststore = gest_completion.get_model()
    gest_filtro = gest_entry.get_text()
    # seleziona i dati in base al filtro
    if filtro=="codice":
        articoli = Articolo().select(codice=gest_filtro)
    elif filtro=="denominazione":
        articoli = Articolo().select(denominazione=gest_filtro)
    elif filtro=="produttore":
        articoli = Articolo().select(produttore=gest_filtro)
    elif filtro=="codiceABarre":
        articoli = Articolo().select(codiceABarre=gest_filtro)
    elif filtro=="codiceArticoloFornitore":
        articoli = Articolo().select(codiceArticoloFornitore=gest_filtro)
    # ripulisco la liststore per evitare accavallamenti
    gest_liststore.clear()
    i = 0
    # aggiorna la liststore con gli oggetti in articoli
    for n in articoli:
        print "Il record " + repr(i) + " contiene: " + n.codice
        if filtro == "codice":
            gest_liststore.append([n.codice, n])
        elif filtro == "denominazione":
            gest_liststore.append([n.denominazione, n])
        elif filtro == "produttore":
            gest_liststore.append([n.produttore, n])
        elif filtro == "codiceABarre":
            gest_liststore.append([n.codice_a_barre, n])
        elif filtro=="codiceArticoloFornitore":
            gest_liststore.append([n.codice_articolo_fornitore, n])
        print gest_liststore[i][0] + " inserita nella liststore"
        i = i + 1
    gest_completion.set_model(gest_liststore)
    gest_entry.set_completion(gest_completion)
