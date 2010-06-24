# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Alceste Scalas <alceste@promotux.it>, Francesco Meloni <francesco@promotux.it>
# License GNU Gplv2

import gtk
from promogest import Environment
from GladeWidget import GladeWidget

class ConfiguraWindow(GladeWidget):

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        GladeWidget.__init__(self, 'configura_window', fileName='configura_window.glade')
        self.placeWindow(self.getTopLevel())

        self.draw()

    def draw(self):
        self.sections_box = gtk.VBox()
        self.sections_box.set_spacing(6)
        sections = Environment.conf.sections()
        i = 0
        for section in sections:
            localFrame = gtk.Frame(section)
            localFrame.set_border_width(8)
            current_section = getattr(Environment.conf, section)

            #get the sections' attributes
            attrs = current_section.options()

            #populate the frame with labels containing the attributes' names
            attr_box = gtk.VBox()

            for attr in attrs:
                attr_hbox = gtk.HBox()
                attr_hbox.set_homogeneous(False)
                label_attribute = gtk.Label(attr)
                label_attribute.set_padding(7, 0)
                label_attribute.set_alignment(0.0, 0.5)
                label_attribute.set_size_request(200, -1)
                attr_hbox.pack_start(label_attribute, False, False)

                #create the entry containing the attribute's value
                entry_valore = gtk.Entry()
                entry_valore.connect('changed', self.on_entry_value_changed, current_section, attr)
                attr_hbox.add(entry_valore)
                attr_value = getattr(current_section, attr)
                if attr == 'password':
                    entry_valore.set_visibility(False)
                entry_valore.set_text(attr_value)

                attr_box.add(attr_hbox)

            localFrame.add(attr_box)
            self.sections_box.add(localFrame)

        self.params_scrolled_window.add_with_viewport(self.sections_box)
        self.salva_button.set_sensitive(False)

    def on_entry_value_changed(self, entry,current_section, attr):
        self.salva_button.set_sensitive(True)
        setattr(current_section,attr,entry.get_text())

    def on_salva_button_clicked(self, button_salva):
        Environment.conf.save()
        self.salva_button.set_sensitive(False)

    def on_quit(self, widget=None, event=None):
        self.destroy()
