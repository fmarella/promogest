# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Authors:
#             Andrea Argiolas <andrea@promotux.it>
#             JJDaNiMoTh <jjdanimoth@gmail.com>
#             Dr astico (Marco Pinna) <marco@promotux.it>
#             Francesco Meloni <francesco@promotux.it>
#             Francesco Marella <francesco.marella@anche.no>

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

import os
import sys
from gi.repository import GLib, Gtk, Poppler
from promogest.lib.utils import *


class PrintingApp(object):
    def __init__(self, fileName, tipo=None):
        self.operation = Gtk.PrintOperation()
        setting = Gtk.PageSetup()

        st = Gtk.PrintSettings()
        s = Gtk.PageSetup()
        if tipo == "singolo":
            ps = Gtk.PaperSize.new_custom("cc", "cc", 210, 297, Gtk.Unit.MM)
            s.set_paper_size(ps)
            margine_fondo = float(setconf("Stampa", "singolo_margine_basso")or 4.3)
            s.set_bottom_margin(margine_fondo, Gtk.Unit.MM)
            margine_sinistro = float(
                setconf("Stampa", "singolo_margine_sinistro")or 4.3)
            s.set_left_margin(margine_sinistro, Gtk.Unit.MM)
            margine_destro = float(
                setconf("Stampa", "singolo_margine_destro")or 4.3)
            s.set_right_margin(margine_destro, Gtk.Unit.MM)
            margine_alto = float(setconf("Stampa", "singolo_margine_alto")or 4.3)
            s.set_top_margin(margine_alto, Gtk.Unit.MM)
            orientamento = str(setconf("Stampa", "singolo_ori"))
            if orientamento == "orizzontale":
                s.set_orientation(Gtk.PageOrientation.LANDSCAPE)
        elif tipo == "report":
            ps = Gtk.PaperSize.new_custom("cc", "cc", 210, 297, Gtk.Unit.MM)
            s.set_paper_size(ps)
            margine_fondo = float(setconf("Stampa", "report_margine_basso") or 4.3
            )
            s.set_bottom_margin(margine_fondo, Gtk.Unit.MM)
            margine_sinistro = float(
                setconf("Stampa", "report_margine_sinistro")or 4.3)
            s.set_left_margin(margine_sinistro, Gtk.Unit.MM)
            margine_destro = float(
                setconf("Stampa", "report_margine_destro")or 4.3)
            s.set_right_margin(margine_destro, Gtk.Unit.MM)
            margine_alto = float(setconf("Stampa", "report_margine_alto")or 4.3)
            s.set_top_margin(margine_alto, Gtk.Unit.MM)
            orientamento = str(setconf("Stampa", "report_ori"))
            if not orientamento or orientamento == "orizzontale":
                s.set_orientation(Gtk.PageOrientation.LANDSCAPE)
        elif tipo =="label":
            from promogest.lib.PyPDF2.pdf import PdfFileReader
            input1 = PdfFileReader(file(fileName))
            input1.getPage(0).mediaBox
            larg = input1.getPage(0).mediaBox[2]
            alte = input1.getPage(0).mediaBox[3]
            ps = Gtk.PaperSize.new_custom("cc", "cc", alte, larg, Gtk.Unit.POINTS)
            s.set_paper_size(ps)
            s.set_right_margin(0, Gtk.Unit.MM)
            s.set_left_margin(0, Gtk.Unit.MM)
            s.set_bottom_margin(0, Gtk.Unit.MM)
            s.set_top_margin(0, Gtk.Unit.MM)
            s.set_orientation(Gtk.PageOrientation.LANDSCAPE)

        self.operation.set_default_page_setup(s)
        self.operation.connect('begin-print', self.begin_print, None)
        self.operation.connect('draw-page', self.draw_page, None)
        file_uri = GLib.filename_to_uri(os.path.abspath(fileName))

        self.doc = Poppler.Document.new_from_file(file_uri)

    def begin_print(self, operation, print_ctx, print_data):
        operation.set_n_pages(self.doc.get_n_pages())

    def draw_page(self, operation, print_ctx, page_num, print_data):
        cr = print_ctx.get_cairo_context()
        page = self.doc.get_page(page_num)
        page.render(cr)

    def run(self, parent=None):
        result = self.operation.run(Gtk.PrintOperationAction.PRINT_DIALOG,
                                    parent)

        if result == Gtk.PrintOperationResult.ERROR:
            message = self.operation.get_error()

            dialog = Gtk.MessageDialog(parent,
                                       0,
                                       Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.CLOSE,
                                       message)

            dialog.run()
            dialog.destroy()
