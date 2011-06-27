# -*- coding: utf-8 -*-

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

from promogest.ui.gtk_compat import *
import time, datetime
from DateEntryField import DateEntryField
from promogest import Environment

class DateWidget(gtk.HBox):
# dateentryfield con possibilita' di scelta dal calendario
    __gtype_name__ = 'DateWidget'
    def __init__(self, str1=None, str2=None, int1=None, int2=None, futurecheck=None):
        self.futurecheck = futurecheck
        gtk.HBox.__init__(self, False, 0)
        self.entry = DateEntryField(str1, str2, int1, int2)
        self.button = gtk.ToggleButton()
        self.button.set_property("can-focus", False)
        image = gtk.Image()
        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'calendario16x16.png')
        image.set_from_pixbuf(pbuf)
        self.button.add(image)
        self.pack_start(self.entry, True, True, 0)
        self.pack_start(self.button, False, False, 0)
        self.button.connect('clicked', self.my_button_clicked)
        self.connect("show", self.on_show)
        self.entry.connect('focus_out_event', self.my_focus_out_event)


    def my_button_clicked(self, button):

        def currentAction(button):
            current = datetime.datetime.now()
            self.calendar.select_month((current.month-1), current.year)
            self.calendar.select_day(current.day)

        def confirmAction(button):
            try:
                (year, month, day) = self.calendar.get_date()
                data = datetime.datetime.now()
                if (year, month+1, day)>(data.year,data.month,data.day) and self.futurecheck==None:
                    msg = "Attenzione, hai selezionato una data futura\nSi desidera forzare la scelta ?"
                    dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                        gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
                    response = dialog.run()
                    dialog.destroy()
                    if response == gtk.RESPONSE_YES:
                        day = '%02d' % int(day)
                        month = '%02d' % int(month + 1)
                        year = '%04d' % int(year)
                        data = day + month + year
                        time.strptime(data, "%d%m%Y")
                        self.entry.set_text(day + '/' + month + '/' + year)
                        window.destroy()
                    else:
                        self.entry.set_text("")
                else:
                    day = '%02d' % int(day)
                    month = '%02d' % int(month + 1)
                    year = '%04d' % int(year)
                    data = day + month + year
                    time.strptime(data, "%d%m%Y")
                    self.entry.set_text(day + '/' + month + '/' + year)
                    window.destroy()
            except Exception:
                return
            self.entry.grab_focus()

        def cancelAction(button):
            window.destroy()
            self.entry.grab_focus()

        def on_destroy(window):
            self.button.set_active(False)
            self.entry.grab_focus()


        if not button.get_active():
            return

        window = gtk.Window()
        window.set_size_request(300, 260)
        window.set_modal(True)
        window.set_transient_for(self.get_toplevel())
        window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        window.set_title('Selezione data')
        window.connect("destroy", on_destroy)
        vbox = gtk.VBox()

        self.calendar = gtk.Calendar()
        currentDate = self.entry.get_text()
        if not(currentDate is None or currentDate == ''):
            try:
                d = time.strptime(currentDate, "%d/%m/%Y")
                self.calendar.select_month((d[1]-1), d[0])
                self.calendar.select_day(d[2])

            except Exception:
                pass

        self.calendar.connect('day-selected-double-click', confirmAction)
        vbox.pack_start(self.calendar, True, True, 0)

        separator = gtk.HSeparator()
        vbox.pack_start(separator, False, False, 5)

        bbox = gtk.HButtonBox()
        buttonCorrente = gtk.Button(label='_Corrente', stock=None, use_underline=True)
        buttonCorrente.connect('clicked', currentAction)
        buttonOk = gtk.Button(label='_Ok', stock=None, use_underline=True)
        buttonOk.connect('clicked', confirmAction)
        buttonAnnulla = gtk.Button(label='_Annulla', stock=None, use_underline=True)
        buttonAnnulla.connect('clicked', cancelAction)
        bbox.add(buttonCorrente)
        bbox.add(buttonOk)
        bbox.add(buttonAnnulla)
        bbox.set_layout(gtk.BUTTONBOX_SPREAD)
        vbox.pack_start(bbox, False, False, 5)

        window.add(vbox)
        window.show_all()


    def get_text(self):
        return self.entry.get_text()


    def set_text(self, stringa=''):
        self.entry.set_text(stringa)


    def setNow(self):
        self.entry.setNow()


    def on_show(self, event):
        (width, heigth) = self.get_size_request()
        if width == -1:
            self.setSize()


    def setSize(self, size=None):
        if size is None:
            size = -1
            parent = self.get_parent()
            if parent is not None:
                if parent.__class__ is gtk.Alignment:
                    (width, heigth) = parent.get_size_request()
                    size = width

        self.set_size_request(size, -1)


    def my_focus_out_event(self, entry, event):
        self.emit('focus_out_event', event)


#gobject.type_register(DateWidget)
