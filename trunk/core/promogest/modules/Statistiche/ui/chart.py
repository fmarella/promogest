# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from numpy import arange, sin, pi
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
from promogest.ui.utils import *
from promogest.ui.gtk_compat import *

class chartViewer():
    def __init__(self,widget, func= None, daos = None):
        member = getattr(self, func)
        self.fig = member(daos=daos)
        self.draw(widget, func)

    def draw(self,widget, func):

        win = gtk.Window()
        win.connect("destroy", lambda x: gtk.main_quit())
        win.set_default_size(800,600)
        win.set_title("Chart statistiche PromoGest2")
        vbox = gtk.VBox()

        win.add(vbox)
        sw = gtk.ScrolledWindow()
        vbox.pack_start(sw, True, True, 0)
        sw.set_border_width (10)
        sw.set_policy (hscrollbar_policy=GTK_POLICYTYPE_AUTOMATIC,
               vscrollbar_policy=GTK_POLICYTYPE_ALWAYS)

        canvas = FigureCanvas(self.fig)  # a gtk.DrawingArea

        sw.add_with_viewport (canvas)
        toolbar = NavigationToolbar(canvas, win)
        toolbar.set_message(func)
        vbox.pack_start(toolbar, False, False, 0)
        win.set_modal(True)
        win.set_transient_for(None)
        win.show_all()
        gtk.main()

    def export_csv(self):
        print "OKOKOKOKKOKOKOKOKO"



    def affluenzaOrariaGiornaliera(self, daos=None):
        """ TODO: Avvisare con un messaggio quando i dati non sono omogenei
            esempio ci sono più giorni negli scontrini """
        ore = []
        if scontrini:
            for sco in daos:
                ore.append(sco.data_inserimento.hour)
        f = plt.figure()
        ax = f.add_subplot(111)

        plt.plot([a for a in range(8,25)], [ore.count(b) or 0 for b in range(8,25)], color='red',label='Q/h',linewidth=2)

        ax.xaxis.set_major_locator(plt.FixedLocator(range(8,25)))
#        ax.yaxis.set_major_locator(plt.FixedLocator(range(0,len(ore)+1)))

        plt.ylabel('Numero scontrini emessi')
        plt.xlabel('Orario 8,00 alle 24,00')

        plt.axis()
        plt.legend()
        plt.grid(True)
        return f

    def graficoPesateInfopeso(self, daos=None):
        """ TODO: Avvisare con un messaggio quando i dati non sono omogenei
            esempio ci sono più giorni negli scontrini """
        ore = []

        f = plt.figure()
        ax = f.add_subplot(111)
        plt.plot([b.data_registrazione for b in daos],[float(a.peso) for a in daos], color='green',label='Peso/Data',linewidth=3)

        plt.ylabel('Pesate')
        plt.xlabel('Data pesate')

        plt.axis()
        plt.legend()
        f.autofmt_xdate()
        plt.grid(True)
        print "COSA SEI ", f, dir(f)
        plt.savefig("/home/vete/node.png")
        return f


    def affluenzaGiornalieraMensile(self, daos=None):
        """ TODO: Avvisare con un messaggio quando i dati non sono omogenei
            esempio ci sono più mesi negli scontrini """
        giorni = []
        if scontrini:
            for sco in scontrini:
                giorni.append(sco.data_inserimento.day)
        f = plt.figure()
        ax = f.add_subplot(111)

        plt.plot([a for a in range(1,32)], [giorni.count(b) or 0 for b in range(0,31)], color='green',label='Q/h',linewidth=2)

        ax.xaxis.set_major_locator(plt.FixedLocator(range(1,32)))
#        ax.yaxis.set_major_locator(plt.FixedLocator(range(0,len(giorni)+1)))

        plt.ylabel('Numero scontrini emessi')
        plt.xlabel('Giorni del mese')

        plt.axis()
        plt.legend()
        plt.grid(True)
        return f

    def affluenzaMensileAnnuale(self, daos=None):
        mesi = []
        if scontrini:
            for sco in daos:
                mesi.append(sco.data_inserimento.month)
        f = plt.figure()
        ax = f.add_subplot(111)

        plt.plot([a for a in range(1,13)], [mesi.count(b) or 0 for b in range(1,13)], color='green',label = 'Q/y',linewidth = 2)

        ax.xaxis.set_major_locator(plt.FixedLocator(range(1,13)))
#        ax.yaxis.set_major_locator(plt.FixedLocator(range(0,len(mesi)+1)))

        plt.ylabel('Numero scontrini emessi')
        plt.xlabel('Mesi')

        plt.axis()
        plt.legend()
        plt.grid(True)
        return f
