# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Francesco Marella <francesco.marella@gmail.com>

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


from promogest import Environment
from promogest.ui.utils import *
from promogest.ui.gtk_compat import *
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
