# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

# Author: Alceste Scalas <alceste@promotux.it>
# Author: Andrea Argiolas <andrea@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it

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

import commands
import os
import shutil
import tempfile
from promogest import Environment
from promogest.ui.gtk_compat import *

if not Environment.pg3:
    try:
        import gtkunixprint
        gtkunixprint # pyflakes
    except ImportError:
        gtkunixprint = None
else:
    gtkunixprint = None


class GtkPrintDialog(object):
    """A dialog to print PDFs using the printer dialog in Gtk+ 2.10+
    """
    def __init__(self, report):
        self._report = report
        self._dialog = self._create_dialog()

    def _create_dialog(self):
        dialog = gtkunixprint.PrintUnixDialog(parent=None)
        dialog.set_manual_capabilities(gtkunixprint.PRINT_CAPABILITY_COPIES |
                                       gtkunixprint.PRINT_CAPABILITY_PAGE_SET)
        #button = self._add_preview_button(dialog)
        #button.connect('clicked', self._on_preview_button__clicked)
        return dialog

    def _add_preview_button(self, dialog):
        # Add a preview button
        button = gtk.Button(stock=gtk.STOCK_PRINT_PREVIEW)
        dialog.action_area.pack_start(button)
        dialog.action_area.reorder_child(button, 0)
        button.show()
        return button

    def _send_to_printer(self, printer, settings, page_setup):
        job = gtkunixprint.PrintJob(self._report, printer,settings, page_setup)
        job.set_source_file(self._report)
        job.send(self._on_print_job_complete)

    def _print_preview(self):
        print_preview(self._report.filename, keep_file=True)

    #
    # Public API
    #

    def run(self):
        response = self._dialog.run()
        if response in [GTK_RESPONSE_CANCEL,
                        GTK_RESPONSE_DELETE_EVENT]:
            self._dialog.destroy()
            self._dialog = None
        elif response == GTK_RESPONSE_OK:
            self._send_to_printer(self._dialog.get_selected_printer(),
                                  self._dialog.get_settings(),
                                  self._dialog.get_page_setup())
            self._dialog.destroy()
            self._dialog = None
        else:
            raise AssertionError("unhandled response: %d" % (response,))

    #
    # Callbacks
    #

    def _on_preview_button__clicked(self, button):
        self._print_preview()

    def _on_print_job_complete(self, job, data, error):
        if error:
            print 'FIXME, handle error:', error
