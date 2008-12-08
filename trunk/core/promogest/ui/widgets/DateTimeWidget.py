# -*- coding: iso-8859-15 -*-

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

import gtk
import time, datetime
from DateTimeEntryField import DateTimeEntryField
from promogest import Environment

class DateTimeWidget(gtk.HBox):
# datetimeentryfield con possibilita' di scelta dal calendario e dall'orario

    def __init__(self, str1=None, str2=None, int1=None, int2=None):
        gtk.HBox.__init__(self, False, 0)
        self.entry = DateTimeEntryField(str1, str2, int1, int2)
        self.button = gtk.ToggleButton()
        self.button.set_property("can-focus", False)
        image = gtk.Image()
        pbuf = gtk.gdk.pixbuf_new_from_file(Environment.conf.guiDir + 'calendario16x16.png')
        image.set_from_pixbuf(pbuf)
        self.button.add(image)
        self.pack_start(self.entry, True, True, 0)
        self.pack_start(self.button, False, False, 0)
        self.button.connect('clicked', self.do_button_clicked)
        self.connect("show", self.on_show)
        self.entry.connect('focus_out_event', self.do_focus_out_event)


    def do_button_clicked(self, button):

        def currentAction(button):
            current = datetime.datetime.now()
            self.calendar.select_month((current.month-1), current.year)
            self.calendar.select_day(current.day)
            self.spinButtonOra.set_value(current.hour)
            self.spinButtonMinuti.set_value(current.minute)

        def confirmAction(button):
            try:
                (year, month, day) = self.calendar.get_date()
                day = '%02d' % int(day)
                month = '%02d' % int(month + 1)
                year = '%04d' % int(year)
                hour = '%02d' % self.spinButtonOra.get_value_as_int()
                minutes = '%02d' % self.spinButtonMinuti.get_value_as_int()
                data_ora = day + month + year + hour + minutes
                time.strptime(data_ora, "%d%m%Y%H%M")
                self.entry.set_text(day + '/' + month + '/' + year + ' ' + hour + ':' + minutes)
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
        window.set_size_request(300, 360)
        window.set_modal(True)
        window.set_transient_for(self.get_toplevel())
        window.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        window.set_title('Selezione data e ora')
        window.connect("destroy", on_destroy)
        vbox = gtk.VBox()

        self.calendar = gtk.Calendar()
        self.spinButtonOra = gtk.SpinButton(digits=0)
        self.spinButtonOra.set_numeric(True)
        self.spinButtonOra.set_wrap(True)
        self.spinButtonOra.set_range(0,23)
        self.spinButtonOra.set_increments(1,1)
        self.spinButtonMinuti = gtk.SpinButton(digits=0)
        self.spinButtonMinuti.set_numeric(True)
        self.spinButtonMinuti.set_wrap(True)
        self.spinButtonMinuti.set_range(0,59)
        self.spinButtonMinuti.set_increments(1,1)

        currentDateTime = self.entry.get_text()
        if not(currentDateTime is None or currentDateTime == ''):
            try:
                d = time.strptime(currentDateTime, "%d/%m/%Y %H:%M")
                self.calendar.select_month((d[1]-1), d[0])
                self.calendar.select_day(d[2])
                self.spinButtonOra.set_value(d[3])
                self.spinButtonMinuti.set_value(d[4])
            except Exception:
                pass

        self.calendar.connect('day-selected-double-click', confirmAction)
        alignment = gtk.Alignment(1, 1, 1, 1)
        alignment.set_padding(6, 2, 2, 2)
        alignment.add(self.calendar)
        frame = gtk.Frame('Data: ')
        frame.set_label_align(0,1)
        frame.set_border_width(6)
        frame.add(alignment)
        vbox.pack_start(frame, True, True, 3)

        separator = gtk.HSeparator()
        vbox.pack_start(separator, False, False, 0)

        hbox = gtk.HBox()
        label = gtk.Label(':')
        hbox.pack_start(self.spinButtonOra, False, False, 0)
        hbox.pack_start(label, False, False, 5)
        hbox.pack_start(self.spinButtonMinuti, False, False, 0)
        alignment = gtk.Alignment(1, 1, 1, 1)
        alignment.set_padding(3, 2, 2, 2)
        alignment.add(hbox)
        frame = gtk.Frame('Ora: ')
        frame.set_label_align(0,1)
        frame.set_border_width(6)
        frame.add(alignment)
        vbox.pack_start(frame, False, False, 5)

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


    def do_focus_out_event(self, entry, event):
        self.emit('focus_out_event', event)


#gobject.type_register(DateTimeWidget)
