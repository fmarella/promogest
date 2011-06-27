# -*- coding: utf8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Marella <francesco.marella@gmail.com>
#    Author: Francesco Meloni  <francesco@promotux.it>

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
if not Environment.pg3:
    try:
        import pygtk
        pygtk.require('2.0')
        import gtk
        from gtk import gdk as gdk
        import pango
        import gobject

        PANGO_ALIGN_LEFT = pango.TAB_LEFT
        GTK_RESPONSE_OK = gtk.RESPONSE_OK
        GTK_RESPONSE_CLOSE = gtk.RESPONSE_CLOSE
        GTK_RESPONSE_CANCEL = gtk.RESPONSE_CANCEL
        GTK_RESPONSE_APPLY = gtk.RESPONSE_APPLY
        GTK_RESPONSE_DELETE_EVENT = gtk.RESPONSE_DELETE_EVENT
        GTK_RESPONSE_YES = gtk.RESPONSE_YES
        GTK_RESPONSE_NO = gtk.RESPONSE_NO
        GTK_RESPONSE_REJECT = gtk.RESPONSE_REJECT
        GTK_DIALOG_MODAL = gtk.DIALOG_MODAL
        GTK_DIALOG_DESTROY_WITH_PARENT = gtk.DIALOG_DESTROY_WITH_PARENT
        GTK_DIALOG_MESSAGE_INFO = gtk.MESSAGE_INFO
        GTK_DIALOG_MESSAGE_QUESTION = gtk.MESSAGE_QUESTION
        GTK_DIALOG_MESSAGE_WARNING = gtk.MESSAGE_WARNING
        GTK_BUTTON_OK = gtk.BUTTONS_OK
        GTK_BUTTON_YES_NO = gtk.BUTTONS_YES_NO


        gtk_status_icon_new = gtk.status_icon_new_from_file
        pango_tabarray_new = pango.TabArray
        gdk_keyval_name = gtk.gdk.keyval_name

        GDK_EVENTTYPE_BUTTON_PRESS = gdk.BUTTON_PRESS
        GDK_EVENTTYPE_2BUTTON_PRESS = gdk._2BUTTON_PRESS
        GDK_EVENTTYPE_3BUTTON_PRESS = gdk._3BUTTON_PRESS

        GDK_EVENTTYPE_KEY_PRESS = gtk.gdk.KEY_PRESS
        GDK_CONTROL_MASK = gtk.gdk.CONTROL_MASK

        GDK_KEY_F5 = gtk.keysyms.F5
        GTK_ACCEL_VISIBLE = gtk.ACCEL_VISIBLE

        GTK_SELECTIONMODE_SINGLE = gtk.SELECTION_SINGLE
        GTK_SELECTIONMODE_MULTIPLE = gtk.SELECTION_MULTIPLE

        GTK_STATE_NORMAL = gtk.STATE_NORMAL
        GDK_COLOR_PARSE = gtk.gdk.color_parse

        GDK_PIXBUF_NEW_FROM_FILE = gtk.gdk.pixbuf_new_from_file
        GTK_WIN_POS_CENTER_ON_PARENT = gtk.WIN_POS_CENTER_ON_PARENT
        GTK_BUTTON_BOX_SPREAD =  gtk.BUTTONBOX_SPREAD

        GOBJECT_SIGNAL_RUNLAST = gobject.SIGNAL_RUN_LAST
        GTK_COLUMN_GROWN_ONLY =  gtk.TREE_VIEW_COLUMN_GROW_ONLY

    except ImportError:
        pass

else:
    import gi
    gi.require_version('Gdk', '3.0')
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gdk as gdk
    from gi.repository import Gtk as gtk
    from gi.repository import Pango as pango
    from gi.repository import GdkPixbuf
    from gi.repository import GObject as gobject
    pygtk = None

    # these are hacks until we fully switch to GI
    PANGO_ALIGN_LEFT = pango.TabAlign.LEFT
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
    GTK_BUTTON_OK = gtk.ButtonsType.OK
    GTK_BUTTON_YES_NO = gtk.ButtonsType.YES_NO


    gtk_status_icon_new = gtk.StatusIcon.new_from_file
    pango_tabarray_new = pango.TabArray.new
    gdk_keyval_name = gdk.keyval_name


    GDK_EVENTTYPE_BUTTON_PRESS = gdk.EventType.BUTTON_PRESS
    GDK_EVENTTYPE_2BUTTON_PRESS = gdk.EventType._2BUTTON_PRESS
    GDK_EVENTTYPE_3BUTTON_PRESS = gdk.EventType._3BUTTON_PRESS

    GDK_EVENTTYPE_KEY_PRESS = gdk.EventType.KEY_PRESS
    GDK_CONTROL_MASK = gdk.ModifierType.CONTROL_MASK

    GDK_KEY_F5 = gdk.KEY_F5
    GTK_ACCEL_VISIBLE = gtk.AccelFlags.VISIBLE

    GTK_SELECTIONMODE_SINGLE = gtk.SelectionMode.SINGLE
    GTK_SELECTIONMODE_MULTIPLE = gtk.SelectionMode.MULTIPLE

    GTK_STATE_NORMAL = gtk.StateType.NORMAL
    GDK_COLOR_PARSE = gdk.color_parse

    GDK_PIXBUF_NEW_FROM_FILE = GdkPixbuf.Pixbuf.new_from_file
    GTK_WIN_POS_CENTER_ON_PARENT = gtk.WindowPosition.CENTER_ON_PARENT
    GTK_BUTTON_BOX_SPREAD = gtk.ButtonBoxStyle.SPREAD

    GOBJECT_SIGNAL_RUNLAST = gobject.SignalFlags.RUN_LAST

    GTK_COLUMN_GROWN_ONLY =  gtk.TreeViewColumnSizing.GROW_ONLY
