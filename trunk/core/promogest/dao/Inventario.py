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
from Articolo import Articolo
from Dao import Dao


class Inventario(Dao):
    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def _unita_base(self):
        if self.arti: return self.arti.denominazione_breve_unita_base
        else: return ""
    denominazione_breve_unita_base= property(_unita_base)

    def _codice_articolo(self):
        if self.arti: return self.arti.codice
        else: return ""
    codice_articolo= property(_codice_articolo)

    def _articolo(self):
        if self.arti: return self.arti.denominazione
        else: return ""
    articolo= property(_articolo)

    def _produttore(self):
        if self.arti: return self.arti.produttore
        else: return ""
    produttore= property(_produttore)

    def _denominazione_famiglia(self):
        if self.arti: return self.arti.denominazione_famiglia
        else: return ""
    denominazione_famiglia= property(_denominazione_famiglia)

    def _denominazione_categoria(self):
        if self.arti: return self.arti.denominazione_categoria
        else: return ""
    denominazione_categoria= property(_denominazione_categoria)

    def _codice_a_barre(self):
        if self.arti: return self.arti.codice_a_barre
        else: return ""
    codice_a_barre= property(_codice_a_barre)

    def _codice_articolo_fornitore(self):
        if self.arti: return self.arti.codice_articolo_fornitore
        else: return ""
    codice_articolo_fornitore= property(_codice_articolo_fornitore)

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

    def control(self,window):
        """ Verifica se esistono gia' delle righe di inventario nell'anno di esercizio """
        res = self.count(anno=Environment.workingYear)
        print "REEEEEEEEEEEEEEEEEEEESSS PER INVENTARIO", res
        if not res :
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

    def giacenzaSel(self, year=None, idMagazzino=None, idArticolo=None):
        from TestataMovimento import TestataMovimento
        from RigaMovimento import RigaMovimento
        from Riga import Riga

        righeArticoloMovimentate= params["session"]\
                .query(RigaMovimento,TestataMovimento)\
                .filter(and_(func.date_part("year", TestataMovimento.data_movimento)==year))\
                .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                .filter(Riga.id_articolo==idArticolo)\
                .filter(Riga.id_magazzino==idMagazzino)\
                .filter(Articolo.cancellato!=True)\
                .all()

        lista = []
        for ram in righeArticoloMovimentate:

            def calcolaGiacenza(quantita=None, moltiplicatore=None, segno=None, valunine=None):
                giacenza=0
                if segno =="-":
                    giacenza -= quantita*moltiplicatore
                else:
                    giacenza += quantita*moltiplicatore
                valore= giacenza*valunine
                return (giacenza, valore)

            diz = {"numero":ram[1].numero,
                    "data_movimento":ram[1].data_movimento,
                    "operazione":ram[1].operazione,
                    "id_articolo":ram[0].id_articolo,
                    "giacenza":calcolaGiacenza(quantita=ram[0].quantita,moltiplicatore=ram[0].moltiplicatore, segno=ram[1].segnoOperazione, valunine=ram[0].valore_unitario_netto)[0],
                    "cliente":ram[1].ragione_sociale_cliente,
                    "fornitore":ram[1].ragione_sociale_fornitore,
                    "valore":calcolaGiacenza(quantita=ram[0].quantita,moltiplicatore=ram[0].moltiplicatore, segno=ram[1].segnoOperazione, valunine=ram[0].valore_unitario_netto)[1],
                    "segnoOperazione":ram[1].segnoOperazione
                    #"test_doc":ram[1].testata_documento.numero
                        }
            lista.append(diz)
        return lista



inventario=Table('inventario',params['metadata'],schema = params['schema'],autoload=True)
std_mapper = mapper(Inventario, inventario,properties={
        "arti":relation(Articolo,primaryjoin=inventario.c.id_articolo==Articolo.id,backref=backref("inve"))}, order_by=inventario.c.id)


