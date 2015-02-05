# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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


class PrintingApp(object):
    def __init__(self, fileName):
        self.operation = Gtk.PrintOperation()

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
