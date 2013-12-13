# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

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


from promogest import Environment
from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *

try:
    t_inventario=Table('inventario',params['metadata'],schema = params['schema'],autoload=True)
except:
    from data.inventario import t_inventario


from promogest.dao.Articolo import Articolo
from promogest.dao.Fornitura import Fornitura
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
from promogest.dao.Dao import Dao
from promogest.lib.utils import YesNoDialog, posso

if hasattr(conf, "PromoWear") and getattr(conf.PromoWear,'mod_enable')=="yes":
    from promogest.modules.PromoWear.dao.Colore import Colore
    from promogest.modules.PromoWear.dao.Taglia import Taglia
    from promogest.modules.PromoWear.dao.ArticoloTagliaColore import ArticoloTagliaColore
    from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
    from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
    from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
    from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento

class Inventario(Dao):
    def __init__(self, req=None):
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
            dic= {k :t_inventario.c.anno == v}
        elif k == 'idMagazzino':
            dic = {k:t_inventario.c.id_magazzino == v}
        elif k == 'idArticolo':
            dic = {k:t_inventario.c.id_articolo == v}
        elif k == 'anno':
            dic = {k:t_inventario.c.anno == v}
        elif k == 'daDataAggiornamento':
            dic = {k:t_inventario.c.data_aggiornamento >= v}
        elif k == 'aDataAggiornamento':
            dic = {k:t_inventario.c.data_aggiornamento <= v}
        elif k == 'qa_zero':
            dic = {k:t_inventario.c.quantita == 0}
        elif k == 'quantita':
            dic = {k:t_inventario.c.quantita > 0}
        elif k == 'qa_negativa':
            dic = {k:t_inventario.c.quantita < 0}
        elif k == 'val_negativo':
            dic = {k:t_inventario.c.valore_unitario == None}
        elif k == 'inventariato':
            dic = {k:t_inventario.c.quantita >= 1}
        elif k == 'articolo':
            dic = {k:and_(t_inventario.c.id_articolo==Articolo.id, Articolo.denominazione.ilike("%"+v+"%"))}
        elif k == 'codice':
            dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.codice.ilike("%"+v+"%"))}
        elif k == 'codiceABarre':
            dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id==CodiceABarreArticolo.id_articolo,CodiceABarreArticolo.codice.ilike("%"+v+"%"))}
        elif k == 'produttore':
            dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.produttore.ilike("%"+v+"%"))}
        elif k== 'codiceArticoloFornitoreEM':
            dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id==Fornitura.id_articolo,Fornitura.codice_articolo_fornitore == v)}
        elif k=='idFamiglia':
            dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id_famiglia_articolo ==v)}
        elif k == 'idCategoria':
            dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id_categoria_articolo ==v)}
        elif k == 'idStato':
            dic= {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id_stato_articolo == v)}
        elif k == 'cancellato':
            dic = {k:or_(and_(t_inventario.c.id_articolo==Articolo.id,Articolo.cancellato != v))}
        elif posso("PW"):
            if k == 'figliTagliaColore':
                dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_articolo_padre==None)}
            elif k == 'idTaglia':
                dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_taglia==v)}
            elif k == 'idModello':
                dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_modello==v)}
            elif k == 'idGruppoTaglia':
                dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_gruppo_taglia ==v)}
            elif k == 'padriTagliaColore':
                dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_articolo_padre!=None)}
            elif k == 'idColore':
                dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_colore ==v)}
            elif k == 'idStagione':
                dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_stagione ==v)}
            elif k == 'idAnno':
                dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_anno == v)}
            elif k == 'idGenere':
                dic = {k:and_(t_inventario.c.id_articolo==Articolo.id,Articolo.id==ArticoloTagliaColore.id_articolo, ArticoloTagliaColore.id_genere ==v)}
        return  dic[k]

    def update(self):
        """ Aggiornamento inventario con gli articoli eventualmente non presenti """
        sel2 = Environment.params['session'].query(Inventario.id_magazzino, Inventario.id_articolo).filter(Inventario.anno ==Environment.workingYear).all()
        sel = Environment.params['session'].query(Magazzino.id, Articolo.id).filter(Articolo.cancellato != True).all()
        for s in sel:
            if s not in sel2:
                inv = Inventario()
                inv.anno = Environment.workingYear
                inv.id_magazzino = s[0]
                inv.id_articolo = s[1]
                inv.persist()

    def control(self,window):

        def calcolaGiacenza(quantita=None, moltiplicatore=None, segno=None, valunine=None):
            giacenza=0
            if segno =="-":
                giacenza -= quantita*moltiplicatore
            else:
                giacenza += quantita*moltiplicatore
            valore= giacenza*valunine
            return (giacenza, valore)

        """ Verifica se esistono gia' delle righe di inventario nell'anno di esercizio """
        res = self.count(anno=Environment.workingYear)
        if not res :
            # richiesta di generazione dell'inventario
            msg = ("Non e' presente nessun caricamento di inventario nell'anno di lavoro:\n\n" +
                "si desidera generarne uno ?")
            if YesNoDialog(msg=msg, transient=window):
                from TestataMovimento import TestataMovimento
                from RigaMovimento import RigaMovimento
                from Riga import Riga
                from Magazzino import Magazzino
                from Articolo import Articolo
                giacenza = 0
                #sel2 = Environment.params['session'].query(Inventario.id_magazzino, Inventario.id_articolo).filter(Inventario.anno ==Environment.workingYear).all()
                sel = Environment.params['session'].query(Magazzino.id, Articolo.id).filter(Articolo.cancellato != True).all()
                for s in sel:
                    righeArticoloMovimentate= params["session"]\
                        .query(RigaMovimento,TestataMovimento)\
                        .filter(and_(func.date_part("year", TestataMovimento.data_movimento)==(int(Environment.workingYear)-1)))\
                        .filter(RigaMovimento.id_testata_movimento == TestataMovimento.id)\
                        .filter(Riga.id_articolo==s[1])\
                        .filter(Riga.id_magazzino==s[0])\
                        .filter(Articolo.cancellato!=True)\
                        .all()

                    for ram in righeArticoloMovimentate:
                        giacenza = calcolaGiacenza(quantita=ram[0].quantita,
                                                    moltiplicatore=ram[0].moltiplicatore,
                                                    segno=ram[1].segnoOperazione,
                                                    valunine=ram[0].valore_unitario_netto)[0]
                        giacenza +=giacenza
                    #if s not in sel2:
                    inv = Inventario()
                    inv.anno = Environment.workingYear
                    inv.id_magazzino = s[0]
                    inv.quantita = giacenza
                    inv.id_articolo = s[1]
                    inv.persist()

                # genera l'inventario per l'anno in corso sulla base delle giacenze finali
                # dell'anno precedente, per ogni magazzino e per ogni articolo

                msg = ("Generazione completata.\n\nEffettuare le dovute modifiche dall'apposita maschera\n" +
                    "di caricamento inventario dopo aver fatto i rilevamenti\n" +
                    "delle merci nei magazzini.\n")
                messageInfoEnv(msg=msg)


std_mapper = mapper(Inventario, t_inventario,properties={
        "arti":relation(Articolo,primaryjoin=t_inventario.c.id_articolo==Articolo.id,backref ="inve")
        }, order_by=t_inventario.c.id)

if tipodb=="sqlite":
    a = session.query(Articolo.id).all()
    b = session.query(Inventario.id_articolo).all()
    fixit =  list(set(b)-set(a))
    print "fixt-inventario", fixit
    for f in fixit:
        aa = Inventario().select(idArticolo=f[0], batchSize=None)
        for a in aa:
            session.delete(a)
        session.commit()
