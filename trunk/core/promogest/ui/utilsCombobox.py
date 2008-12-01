# -*- coding: iso-8859-15 -*-

"""
 Promogest
 Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
 Author: Andrea Argiolas <andrea@promotux.it>
 Author: Francesco Meloni <francesco@promotux.it>
 License: GNU GPLv2
"""


import gobject, os, decimal
from decimal import *
import pygtk
pygtk.require('2.0')
import gtk
import time, datetime
from promogest import Environment

from promogest.dao.TipoAliquotaIva import TipoAliquotaIva
from promogest.dao.Operazione import Operazione
from promogest.dao.Azienda import Azienda
from promogest.dao.TipoRecapito import TipoRecapito
from promogest.dao.RoleAction import RoleAction
from sqlalchemy.orm import *
from sqlalchemy import *
#from utils import leggiAgente
import string, re
import xml.etree.cElementTree as ElementTree
from xml.etree.cElementTree import *
import Login
from promogest.dao.Dao import Dao

# Letture per recuperare velocemente dati da uno o piu' dao correlati



# Riempimento lookup combobox


def fillComboboxAliquoteIva(combobox, filter=False):
    """
    Crea l'elenco delle aliquote iva
    """
    from promogest.dao.AliquotaIva import AliquotaIva
    model = gtk.ListStore(object, int, str)
    ivas = AliquotaIva(isList=True).select(offset=None,batchSize=None)
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
    res = TipoAliquotaIva(isList=True).select(offset=None,batchSize=None)
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
    cats = CategoriaArticolo(isList=True).select(offset=None,batchSize=None)
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
    fams = FamigliaArticolo(isList=True).select(offset=None,batchSize=None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append(None, (None, 0, emptyRow))




    def recurse_tree(id_padre, parent_iter=None, max_depth=None):
        if parent_iter is None :
            padre = None
            path = 0
            for row in model:
                if row[0] is None:
                    path += 1
                    continue
                if row[0].id == id_padre:
                    padre = model.get_iter(path)
                else:
                    iter = model.get_iter(path)
                    if model.iter_has_child(iter):
                        new_depth = model.iter_n_children(iter) or 0
                        if new_depth > 0:
                            padre = recurse_tree(id_padre, iter, new_depth)
                if padre is not None:
                    break
                else:
                    path += 1
        else:
            padre = None
            child_index = 0
            #if model.iter_has_child(parent_iter):
            while child_index < max_depth:
                child_iter = model.iter_nth_child(parent_iter, child_index)
                if model[child_iter][0].id == id_padre:
                    padre = child_iter
                    break
                else:
                    if model.iter_has_child(child_iter):
                        new_depth = model.iter_n_children(parent_iter) or 0
                        if new_depth > 0:
                            padre = recurse_tree(id_padre, child_iter, new_depth)
                    if padre is not None:
                        break
                child_index += 1
        return padre



    for f in fams:
        if f.id_padre is None:
            node = model.append(None, (f, f.id, f.denominazione))
    for f in fams:
        if f.id_padre is not None:
            padre = recurse_tree(f.id_padre)
            node = model.append(padre, (f, f.id, f.denominazione))

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
    imbs = Imballaggio(isList=True).select(offset=None,batchSize=None)
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
    stas = StatoArticolo(isList=True).select(offset=None,batchSize=None)
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
    res = UnitaBase(isList=True).select(offset=None,batchSize=None)
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
    from promogest.dao.Role import Role
    res = Role(isList=True).select(offset=None,batchSize=None)
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
    Crea l'elenco dei ruoli
    """
    from promogest.dao.Language import Language
    res = Language(isList=True).select(offset=None,batchSize=None)
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
    res = UnitaBase(isList=True).select(offset=None,batchSize=None)
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
    cats = CategoriaCliente(isList=True).select(offset=None,batchSize=None)

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
    cats = CategoriaContatto(isList=True).select(offset=None,batchSize=None)

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
    cats = CategoriaFornitore(isList=True).select(offset=None,batchSize=None)
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
    muls = Multiplo(isList=True).select(offset=None,batchSize=None)
    if not filter:
        emptyRow = ''
    else:
        emptyRow = '< Tutti >'
    model.append((None, 0, emptyRow, 0))

    if noSottoMultipli:
        muls = [ item for item in muls if item.moltiplicatore > 1 ]

    for m in muls:
        model.append((m, m.id, m.denominazione, m.moltiplicatore))

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
    model = gtk.ListStore(gobject.TYPE_PYOBJECT, int, str)
    #liss = Listino().select(Environment.connection,
                                        #denominazione=None,
                                        #orderBy = None,
                                        #offset = None,
                                        #batchSize = None,
                                        #immediate = True)
    liss= Listino(isList=True).select(denominazione=None,offset=None,orderBy = None,batchSize=None)

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

def listinoCandidateSel(OrderBy=None,idArticolo=None,idMagazzino=None,idCliente=None):
    from promogest.dao.Listino import Listino
    from promogest.dao.ListinoMagazzino import ListinoMagazzino
    from promogest.dao.ListinoArticolo import ListinoArticolo
    from promogest.dao.ListinoCategoriaCliente import ListinoCategoriaCliente
    from promogest.dao.ClienteCategoriaCliente import ClienteCategoriaCliente
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
    if not OrderBy:
        OrderBy= "denominazione"

    listinoSelezionato = Listino(isList=True).select(complexFilter=and_(filter1,filter2,filter3), orderBy=OrderBy)
    print "LISTINI ASSOCIATI:", listinoSelezionato
    return listinoSelezionato

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
    for l in liss:
        model.append((l, l.id, (l.denominazione or '')[0:20]))

    combobox.clear()
    renderer = gtk.CellRendererText()
    combobox.pack_start(renderer, True)
    combobox.add_attribute(renderer, 'text', 2)
    combobox.set_model(model)
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(2)

def fillComboboxFornitori(combobox,filter=False, noempty=False):
    """
    Crea l'elenco dei fornitori in un menu a cascata
    """
    from promogest.dao.Fornitore import Fornitore
    model = gtk.ListStore(gobject.TYPE_PYOBJECT, int, str)
    forns = Fornitore(isList=True).select(offset=None,batchSize=None)
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
    """
    Crea l'elenco dei magazzini
    """
    from promogest.dao.Magazzino import Magazzino
    model = gtk.ListStore(object, int, str)
    mags = Magazzino(isList=True).select(offset=None,batchSize=None)
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
    Crea l'elenco delle operazioni per la movimentazione di magazzino
    """
    if tipo:
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
    """
    Crea l'elenco dei tipi di recapito per i contatti
    """
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
    res = TipoRecapito(isList=True).select(orderBy="denominazione")
    model = gtk.ListStore(str)
    model.append(('', ))
    for r in res:
        model.append((r.denominazione, ))
    return model


def fillComboboxAziende(combobox, filter=False):
    """ Crea l'elenco delle aziende  """

    model = gtk.ListStore(object, str, str)
    res = Azienda(isList=True).select(offset=None,batchSize=None, orderBy="schemaa")
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
    pags = Pagamento(isList=True).select(offset=None,batchSize=None)
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
    bans = Banca(isList=True).select(offset=None,batchSize=None)
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
    """
    Crea elenco delle causali di trasporto
    """
    #queryString = ('SELECT DISTINCT causale_trasporto FROM ' + Environment.connection._schemaAzienda + '.testata_documento ORDER BY causale_trasporto')
    #argList = []
    #Environment.connection._cursor.execute(queryString, argList)
    #res = Environment.connection._cursor.fetchall()
    from promogest.dao.TestataDocumento import TestataDocumento
    res = TestataDocumento(isList=True).select(batchSize=None, offset=None,orderBy='causale_trasporto')
    model = gtk.ListStore(object, str)

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
    if combobox.__class__ is gtk.ComboBoxEntry:
        combobox.set_text_column(1)

def fillComboboxAspettoEsterioreBeni(combobox, filter=False):
    """
    Crea elenco degli aspetti esteriori beni
    """
    #queryString = ('SELECT DISTINCT aspetto_esteriore_beni FROM ' + Environment.connection._schemaAzienda + '.testata_documento ORDER BY aspetto_esteriore_beni')
    #argList = []
    #Environment.connection._cursor.execute(queryString, argList)
    #res = Environment.connection._cursor.fetchall()
    from promogest.dao.TestataDocumento import TestataDocumento
    res = TestataDocumento(isList=True).select(batchSize=None, offset=None,orderBy='aspetto_esteriore_beni')
    model = gtk.ListStore(object, str)

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
    """
    Crea l'elenco dei porti trasporto
    """
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
    """
    Crea l'elenco delle destinazioni merce
    """
    from promogest.dao.DestinazioneMerce import DestinazioneMerce
    model = gtk.ListStore(object, int, str)
    dems = DestinazioneMerce(isList=True).select(batchSize=None,offset=None )
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
    """
    Crea l'elenco degli autori gia'inseriti
    """
    from promogest.dao.Promemoria import Promemoria
    argList = []
    autors = Promemoria(isList=True).select(orderBy="autore")
    model = gtk.ListStore(str)
    for a in autors:
        argList.append(a.autore)
    b = list(set(argList))
    for c in b:
        model.append([c])
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
    argList = []
    model = gtk.ListStore(str)
    autors = Promemoria(isList=True).select(orderBy="incaricato")
    for a in autors:
        argList.append(a.incaricato)
    b = list(set(argList))
    for  c in b:
        model.append([c])

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

def getDateRange(string):
    """
    returns a set of two timestamps one at beginning and at the end of
    the year indicated by string (it must be placed on the last 4 characters of the string) (01/01/YEAR, 31/12/YEAR)
    """
    capodanno = '01/01/'+string[-4:]
    san_silvestro = '31/12/'+string[-4:]
    begin_date = stringToDate(capodanno)
    end_date = stringToDate(san_silvestro)
    return (begin_date, end_date)


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
