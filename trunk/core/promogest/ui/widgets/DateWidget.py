# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Andrea Argiolas <andrea@promotux.it>
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

from promogest.ui.gtk_compat import *
import time, datetime
from DateEntryField import DateEntryField
from promogest import Environment


class DateWidget(gtk.HBox):
# dateentryfield con possibilita' di scelta dal calendario
    __gtype_name__ = 'DateWidget'
    def __init__(self, str1=None, str2=None, int1=None, int2=None, futurecheck=None):
        self.futurecheck = futurecheck
        gtk.HBox.__init__(self)
        self.entry = DateEntryField(str1, str2, int1, int2)
        self.button = gtk.ToggleButton()
        self.button.set_property("can-focus", False)
        self.button2 = gtk.Button()
        self.button2.set_property("can-focus", False)
        image = gtk.Image()
        pbuf = GDK_PIXBUF_NEW_FROM_FILE(Environment.guiDir + 'calendario16x16.png')
        image.set_from_pixbuf(pbuf)
        image2 = gtk.Image()
        pbuf2 = GDK_PIXBUF_NEW_FROM_FILE(Environment.guiDir + 'conferma12x12.png')
        image2.set_from_pixbuf(pbuf2)
        self.button.add(image)
        self.button2.add(image2)
        self.pack_start(self.entry, True, True, 0)
        self.pack_start(self.button, False, False, 0)
        self.pack_start(self.button2, False, False, 0)
        self.button.connect('clicked', self.my_button_clicked)
        self.button2.connect('clicked', self.insert_today)
        self.connect("show", self.on_show)
        self.entry.connect('focus_out_event', self.my_focus_out_event)



    def insert_today(self, button):
        current = datetime.datetime.now()
        self.entry.set_text(str(current.day) + '/' + str(current.month) + '/' + str(current.year))

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
                    dialog = gtk.MessageDialog(None, GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT,
                                        GTK_DIALOG_MESSAGE_QUESTION, GTK_BUTTON_YES_NO, msg)
                    response = dialog.run()
                    dialog.destroy()
                    if response == GTK_RESPONSE_YES:
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
        window.set_position(GTK_WIN_POS_CENTER_ON_PARENT)
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
        bbox.set_layout(GTK_BUTTON_BOX_SPREAD)
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
        #self.emit('focus_out_event', event)
        event = GDK_EVENT(GDK_EVENTTYPE_FOCUS_CHANGE)
        event.window = entry.get_window()  # the gtk.gdk.Window of the widget
        event.send_event = True  # this means you sent the event explicitly
        event.in_ = False  # False for focus out, True for focus in


#gobject.type_register(DateWidget)
