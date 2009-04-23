# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

import gtk
import gobject
from promogest import Environment
from promogest.ui.utils import *
from promogest.modules.PromoWear.ui.PromowearUtils import *

def hidePromoWear(ui):
    """ Hide and destroy labels and button if promowear is not present
    """
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


def setLabelInfo(ui):
    """ Setta a stringa vuota le info specifiche dell'articolo promowear
    """
    ui.gruppo_taglia_label.set_markup('<span weight="bold">%s</span>' % ('',))
    ui.taglia_label.set_markup('<span weight="bold">%s</span>' % ('',))
    ui.colore_label.set_markup('<span weight="bold">%s</span>' % ('',))
    ui.stagione_label.set_markup('<span weight="bold">%s</span>' % ('',))
    ui.anno_label.set_markup('<span weight="bold">%s</span>' % ('',))
    ui.tipo_label.set_markup('<span weight="bold">%s</span>' % ('',))

def fillLabelInfo(ui, articolo):
    ui.gruppo_taglia_label.set_markup('<span weight="bold">%s</span>' % (articolo['gruppoTaglia']))
    ui.taglia_label.set_markup('<span weight="bold">%s</span>' % (articolo['taglia']))
    ui.colore_label.set_markup('<span weight="bold">%s</span>' % (articolo['colore']))
    ui.stagione_label.set_markup('<span weight="bold">%s</span>' % (articolo['stagione']))
    ui.anno_label.set_markup('<span weight="bold">%s</span>' % (articolo['anno']))
    ui.tipo_label.set_markup('<span weight="bold">%s</span>' % (""))

def azzeraRiga(anaedit, numero):
    anaedit._righe[numero].update(idGruppoTaglia =  None,
                    gruppoTaglia =  '',
                    idTaglia = None,
                    taglia = '',
                    idColore = None,
                    colore = '',
                    idAnno = None,
                    anno = '',
                    idStagione = None,
                    stagione = '',
                    idGenere = None,
                    genere = '')
