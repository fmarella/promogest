# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2015 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@anche.no>
#    Author: Francesco Meloni  <francesco@promotux.it>

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

# modified from: gtimelog/main.py
# we have to try pygtk first, then fall back to GI; if we have a too old GI
# (without require_version()), we can't import pygtk on top of gi.repo.Gtk.

from promogest import Environment

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk as gdk
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
from gi.repository import Pango as pango
from gi.repository import GLib as glib
#from gi.repository import Cairo as cairo
from gi.repository import GdkPixbuf
pygtk = None

GTK_VERSION = str(gtk.get_major_version()) \
            + '.' \
            + str(gtk.get_minor_version()) \
            + '.' \
            + str(gtk.get_micro_version())

# these are hacks until we fully switch to GI

try:
    PANGO_ALIGN_LEFT = pango.TabAlign.LEFT
except AttributeError:
    # backwards compat for older Pango versions with broken GIR
    PANGO_ALIGN_LEFT = pango.TabAlign.TAB_LEFT
GTK_RESPONSE_OK = gtk.ResponseType.OK
GTK_RESPONSE_CLOSE = gtk.ResponseType.CLOSE
GTK_RESPONSE_CANCEL = gtk.ResponseType.CANCEL
GTK_RESPONSE_APPLY = gtk.ResponseType.APPLY
GTK_RESPONSE_DELETE_EVENT = gtk.ResponseType.DELETE_EVENT
GTK_RESPONSE_YES = gtk.ResponseType.YES
GTK_RESPONSE_NO = gtk.ResponseType.NO
GTK_RESPONSE_REJECT = gtk.ResponseType.REJECT
GTK_DIALOG_MODAL = gtk.DialogFlags.MODAL
GTK_DIALOG_DESTROY_WITH_PARENT = gtk.DialogFlags.DESTROY_WITH_PARENT
GTK_DIALOG_MESSAGE_INFO = gtk.MessageType.INFO
GTK_DIALOG_MESSAGE_QUESTION = gtk.MessageType.QUESTION
GTK_DIALOG_MESSAGE_WARNING = gtk.MessageType.WARNING
GTK_DIALOG_MESSAGE_ERROR = gtk.MessageType.ERROR
GTK_BUTTON_OK = gtk.ButtonsType.OK
GTK_BUTTON_YES_NO = gtk.ButtonsType.YES_NO
GTK_BUTTON_CANCEL = gtk.ButtonsType.CANCEL

gtk_status_icon_new = gtk.StatusIcon.new_from_file
pango_tabarray_new = pango.TabArray.new
gdk_keyval_name = gdk.keyval_name

GTK_COMBOBOXTEXT = gtk.ComboBoxText

GTK_IMAGE_NEW_FROM_STOCK = gtk.Image.new_from_stock

GDK_EVENTTYPE_BUTTON_PRESS = gdk.EventType.BUTTON_PRESS
GDK_EVENTTYPE_2BUTTON_PRESS = gdk.EventType._2BUTTON_PRESS
GDK_EVENTTYPE_3BUTTON_PRESS = gdk.EventType._3BUTTON_PRESS

GDK_EVENTTYPE_KEY_PRESS = gdk.EventType.KEY_PRESS
GDK_EVENTTYPE_FOCUS_CHANGE = gdk.EventType.FOCUS_CHANGE
GDK_EVENT = gdk.Event
GDK_EVENT_DESTROY = gdk.EventType.DESTROY

GDK_CONTROL_MASK = gdk.ModifierType.CONTROL_MASK
GDK_MOD1_MASK = gdk.ModifierType.MOD1_MASK

GDK_KEY_F1 = gdk.KEY_F1
GDK_KEY_F2 = gdk.KEY_F2
GDK_KEY_F3 = gdk.KEY_F3
GDK_KEY_F4 = gdk.KEY_F4
GDK_KEY_F5 = gdk.KEY_F5
GDK_KEY_ESCAPE = gdk.KEY_Escape
GTK_ACCEL_VISIBLE = gtk.AccelFlags.VISIBLE

GTK_SELECTIONMODE_SINGLE = gtk.SelectionMode.SINGLE
GTK_SELECTIONMODE_MULTIPLE = gtk.SelectionMode.MULTIPLE
GTK_SELECTIONMODE_NONE = gtk.SelectionMode.NONE

GTK_STATE_NORMAL = gtk.StateType.NORMAL

GDK_COLOR_PARSE = gdk.color_parse

GDK_PIXBUF_NEW_FROM_FILE = GdkPixbuf.Pixbuf.new_from_file
GTK_WIN_POS_CENTER_ON_PARENT = gtk.WindowPosition.CENTER_ON_PARENT
GTK_BUTTON_BOX_SPREAD = gtk.ButtonBoxStyle.SPREAD

GOBJECT_SIGNAL_RUNLAST = gobject.SignalFlags.RUN_LAST

GTK_COLUMN_GROWN_ONLY = gtk.TreeViewColumnSizing.GROW_ONLY
GTK_COLUMN_FIXED = gtk.TreeViewColumnSizing.FIXED

GTK_ICON_SIZE_BUTTON = gtk.IconSize.BUTTON
GTK_ICON_SIZE_DIALOG = gtk.IconSize.DIALOG
GTK_ICON_SIZE_SMALL_TOOLBAR = gtk.IconSize.SMALL_TOOLBAR

GTK_ATTACHOPTIONS_FILL = gtk.AttachOptions.FILL
GTK_ATTACHOPTIONS_EXPAND = gtk.AttachOptions.EXPAND

GTK_POLICYTYPE_AUTOMATIC = gtk.PolicyType.AUTOMATIC
GTK_JUSTIFICATION_LEFT = gtk.Justification.LEFT

GTK_WINDOWTYPE_TOPLEVEL = gtk.WindowType.TOPLEVEL

GTK_WRAPMODE_WORD = gtk.WrapMode.WORD

GTK_FILE_CHOOSER_ACTION_OPEN = gtk.FileChooserAction.OPEN
GTK_FILE_CHOOSER_ACTION_SAVE = gtk.FileChooserAction.SAVE
GTK_ORIENTATION_VERTICAL = gtk.Orientation.VERTICAL
