# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Andrea Argiolas <andrea@promotux.it>


import gtk
from promogest import Environment
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao


class Inventario(Dao):
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        if k == 'denominazione':
            dic= {  k : inventario.c.anno == v}
        elif k == 'idMagazzino':
            dic = {k:inventario.c.id_magazzino == v}
        elif k == 'idArticolo':
            dic = {k:inventario.c.id_articolo == v}
        elif k == 'anno':
            dic = {k:inventario.c.anno == v}
        elif k == 'daDataAggiornamento':
            dic = {k:inventario.c.data_aggiornameno >= v}
        elif k == 'aDataAggiornamento':
            dic = {k:inventario.c.data_aggiornameno >= v}
        return  dic[k]

inventario=Table('inventario',params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(Inventario, inventario, order_by=inventario.c.id)


def control(window):
    """ Verifica se esistono gia' delle righe di inventario nell'anno di esercizio """
    res = count(anno=Environment.conf.workingYear)

    if res == 0:
        # richiesta di generazione dell'inventario
        msg = ("Non e' presente nessun caricamento di inventario nell'anno di lavoro:\n\n" +
               "si desidera generarne uno ?")
        dialog = gtk.MessageDialog(window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_YES:
            # genera l'inventario per l'anno in corso sulla base delle giacenze finali 
            # dell'anno precedente, per ogni magazzino e per ogni articolo
            Environment.connection.execStoredProcedure('InventarioFill', (int(Environment.conf.workingYear),))

            msg = ("Generazione completata.\n\nEffettuare le dovute modifiche dall'apposita maschera\n" +
                   "di caricamento inventario dopo aver fatto i rilevamenti\n" +
                   "delle merci nei magazzini.\n")
            dialog = gtk.MessageDialog(window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_INFO, gtk.BUTTONS_OK, msg)
            response = dialog.run()
            dialog.destroy()

