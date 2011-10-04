# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                       di Francesco Meloni snc - http://www.promotux.it/

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

from sqlalchemy import Table, or_
from sqlalchemy.orm import mapper, relation, join
from promogest.Environment import params, conf, session
from Dao import Dao
from CategoriaFornitore import CategoriaFornitore
from promogest.modules.Contatti.dao.Contatto import Contatto
from promogest.ui.utils import  codeIncrement, getRecapitiFornitore

class Fornitore(Dao):

    def __init__(self, arg=None):
        Dao.__init__(self, entity=self)

    def _categoria(self):
        a =  params["session"].query(CategoriaFornitore).with_parent(self).filter(self.id_categoria_fornitore==CategoriaFornitore.id).all()
        if not a:
            return a
        else:
            return a[0].denominazione
    categoria = property(_categoria)

    def _cellularePrincipale(self):
        for reca in getRecapitiFornitore(self.id):
            if reca.tipo_recapito =="Cellulare":
                return reca.recapito
        return ""
    cellulare_principale = property(_cellularePrincipale)

    def _telefonoPrincipale(self):
        for reca in getRecapitiFornitore(self.id):
            if reca.tipo_recapito =="Telefono":
                return reca.recapito
        return ""
    telefono_principale = property(_telefonoPrincipale)

    def _emailPrincipale(self):
        for reca in getRecapitiFornitore(self.id):
            if reca.tipo_recapito =="Email":
                return reca.recapito
        return ""
    email_principale = property(_emailPrincipale)

    def _faxPrincipale(self):
        for reca in getRecapitiFornitore(self.id):
            if reca.tipo_recapito =="Fax":
                return reca.recapito
        return ""
    fax_principale = property(_faxPrincipale)

    def _sitoPrincipale(self):
        for reca in getRecapitiFornitore(self.id):
            if reca.tipo_recapito =="Sito":
                return reca.recapito
        return ""
    sito_principale = property(_sitoPrincipale)


    def delete(self):
        categ = self._categoria()
        if categ:
            for c in categ:
                c.delete()
        session.delete(self)
        session.commit()




    def filter_values(self,k,v):
        if k == 'codice':
            dic = {k:persona_giuridica.c.codice.ilike("%"+v+"%")}
        elif k == 'codicesatto':
            dic = {k:persona_giuridica.c.codice == v}
        elif k == 'ragioneSociale':
            dic = {k:persona_giuridica.c.ragione_sociale.ilike("%"+v+"%")}
        elif k == 'insegna':
            dic = {k:persona_giuridica.c.insegna.ilike("%"+v+"%")}
        elif k == 'cognomeNome':
            dic = {k:or_(persona_giuridica.c.cognome.ilike("%"+v+"%"),persona_giuridica.c.nome.ilike("%"+v+"%"))}
        elif k == 'localita':
            dic = {k:or_(persona_giuridica.c.sede_operativa_localita.ilike("%"+v+"%"),persona_giuridica.c.sede_legale_localita.ilike("%"+v+"%"))}
        elif k == 'partitaIva':
            dic = {k:persona_giuridica.c.partita_iva.ilike("%"+v+"%")}
        elif k == 'codiceFiscale':
            dic = {k:persona_giuridica.c.codice_fiscale.ilike("%"+v+"%")}
        elif k == 'idCategoria':
            dic = {k:fornitore.c.id_categoria_fornitore==v}
        return  dic[k]

def getNuovoCodiceFornitore():
    """ Restituisce il codice progressivo per un nuovo fornitore """

    lunghezzaCodice = 8
    prefissoCodice = 'FO'
    codice = ''
    listacodici = []
#    if hasattr(conf,'Fornitori'):
    try:
        forni = session.query(Fornitore.codice).all()[-500:]
        forni.reverse()

        for q in forni:
            codice = codeIncrement(q[0])
            if not codice or Fornitore().select(codicesatto=codice):
                continue
            else:
                if not Fornitore().select(codicesatto=codice):
                    return codice




        #n = 1
        #quanti = session.query(Fornitore).count()
        #if quanti > 0:
            #while session.query(Fornitore).order_by(Fornitore.id.asc()).offset(quanti-n).limit(1).all():
                #art = session.query(Fornitore).order_by(Fornitore.id.asc()).offset(quanti-n).limit(1).all()
                #codice = codeIncrement(art[0].codice)
                #if not codice or Fornitore().select(codicesatto=codice):
                    #if n < 200:
                        #n =n+1
                    #else:
                        #break
                #else:
                    #if not Fornitore().select(codicesatto=codice):
                        #return codice
    except:
        pass
    try:
        if not codice:
            if hasattr(conf,"Fornitori") and hasattr(conf.Fornitori,"struttura_codice"):
                dd = conf.Fornitori.struttura_codice
            else:
                dd = "FO0000"
            codice = codeIncrement(dd)
    except:
        pass

#        try:
##            codicesel = Fornitore().select(batchSize=None, orderBy=Fornitore.ragione_sociale)
#            codicesel  = session.query(Fornitore).all()[-3:]
#            for cod in codicesel:
#                listacodici.append(cod.codice)
#                codice = codeIncrement(str(max(listacodici)))
#        except:
#            pass
#        try:
#            if ( not codice or codice == "")  and hasattr(conf.Fornitori,'struttura_codice'):
#                codice = codeIncrement(conf.Fornitori.struttura_codice)
#        except:
#            pass
    return codice

fornitore=Table('fornitore',params['metadata'],schema = params['schema'],autoload=True)

persona_giuridica=Table('persona_giuridica',params['metadata'],schema = params['schema'],autoload=True)

j = join(fornitore, persona_giuridica)

std_mapper = mapper(Fornitore,j, properties={
        'id':[fornitore.c.id, persona_giuridica.c.id],
        "categoria_fornitore":relation(CategoriaFornitore,backref="fornitore")
        }, order_by=fornitore.c.id)
