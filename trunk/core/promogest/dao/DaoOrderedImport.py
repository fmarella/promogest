# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2014 by Promotux
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

#from sqlalchemy import *
#from sqlalchemy.orm import *
#from promogest.Environment import *
#from promogest.dao.DaoUtils import get_columns
#from sqlalchemy import *
#from sqlalchemy.orm import *
#from promogest.lib.alembic.migration import MigrationContext
#from promogest.lib.alembic.operations import Operations
#from promogest.lib.alembic import op

def orderedImport():
    return
    from promogest.dao.Azienda import Azienda #v
    from promogest.dao.Language import Language #v
    from promogest.modules.RuoliAzioni.dao.Role import Role #v
    from promogest.dao.User import User #v
    #colonne_utente = colonne = get_columns(User.__table__)
    #print "COLONNNNE", colonne_utente,"mailing_list" not in colonne_utente
    #if "mailing_list" not in colonne_utente:
        #try:
            #conn = engine.connect()
            #ctx = MigrationContext.configure(conn)
            #op = Operations(ctx)
            #op.add_column('utente', Column('mailing_list', Boolean, default=False), schema=params["mainSchema"])
        #except:
            #delete_pickle()
    #if "privacy" not in colonne_utente:
        #try:
            #conn = engine.connect()
            #ctx = MigrationContext.configure(conn)
            #op = Operations(ctx)
            #op.add_column('utente', Column('privacy', Boolean, default=False),schema=params["mainSchema"])
        #except:
            #delete_pickle()
    #from promogest.dao.Regioni import t_regione
    from promogest.modules.RuoliAzioni.dao.Action import Action  #v
    from promogest.modules.RuoliAzioni.dao.RoleAction import RoleAction
    from promogest.dao.Access import Access
    from promogest.dao.Setting import Setting
    from promogest.dao.Promemoria import Promemoria
    from promogest.dao.Setconf import * #verificare
    from promogest.dao.Pagamento import Pagamento #v
    from promogest.dao.Operazione import Operazione #v
    from promogest.dao.TipoAliquotaIva import TipoAliquotaIva #v
    from promogest.dao.daoContatti.TipoRecapito import TipoRecapito
    from promogest.dao.UnitaBase import UnitaBase
    from promogest.dao.StatoArticolo import StatoArticolo #v
    from promogest.dao.AliquotaIva import AliquotaIva #v
    from promogest.dao.CategoriaArticolo import CategoriaArticolo #v
    from promogest.dao.Banca import Banca
    from promogest.dao.BancheAzienda import BancheAzienda
    from promogest.dao.FamigliaArticolo import FamigliaArticolo #v
    #from promogest.dao.Image import * # ???????????????????
    from promogest.dao.CategoriaCliente import CategoriaCliente #v
    from promogest.dao.CategoriaFornitore import CategoriaFornitore
    from promogest.dao.Magazzino import Magazzino

    from promogest.dao.Imballaggio import Imballaggio
    from promogest.dao.Listino import Listino #v
    from promogest.dao.Articolo import Articolo #v
    from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
    from promogest.dao.ListinoArticolo import ListinoArticolo
    from promogest.dao.Multiplo import Multiplo #v

    from promogest.dao.ListinoComplessoListino import ListinoComplessoListino
    from promogest.dao.ListinoComplessoArticoloPrevalente import ListinoComplessoArticoloPrevalente
    from promogest.dao.VariazioneListino import VariazioneListino

    from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto
    from promogest.dao.daoContatti.CategoriaContatto import CategoriaContatto
    from promogest.dao.daoContatti.ContattoCategoriaContatto import ContattoCategoriaContatto
    from promogest.dao.daoContatti.Contatto import Contatto #v

    from promogest.dao.Promemoria import Promemoria
    from promogest.dao.Stoccaggio import Stoccaggio #v
    from promogest.dao.PersonaGiuridica import PersonaGiuridica_
    from promogest.dao.PersonaGiuridicaPersonaGiuridica import PersonaGiuridicaPersonaGiuridica



    from promogest.dao.Vettore import Vettore #v
    from promogest.dao.ListinoMagazzino import ListinoMagazzino

    from promogest.dao.Cliente import Cliente
    from promogest.dao.Fornitore import Fornitore
    from promogest.dao.Fornitura import Fornitura
    from promogest.dao.daoAgenti.Agente import Agente #v
    from promogest.dao.ClienteCategoriaCliente import ClienteCategoriaCliente #v
    from promogest.dao.ClienteVariazioneListino import ClienteVariazioneListino #v
    from promogest.dao.Sconto import Sconto
    from promogest.dao.daoContatti.RecapitoContatto import RecapitoContatto
    from promogest.dao.daoContatti.ContattoCliente import ContattoCliente
    from promogest.dao.daoContatti.ContattoFornitore import ContattoFornitore
    from promogest.dao.daoContatti.ContattoAzienda import ContattoAzienda
    from promogest.dao.daoContatti.ContattoMagazzino import ContattoMagazzino
    from promogest.dao.daoContatti.ContattoCategoriaContatto import ContattoCategoriaContatto

    from promogest.dao.Riga import Riga
    #from promogest.dao.AccountEmail import t_account_email

    from promogest.dao.TestataDocumento import TestataDocumento
    from promogest.dao.TestataMovimento import TestataMovimento
    from promogest.dao.RigaDocumento import RigaDocumento
    from promogest.dao.RigaMovimento import RigaMovimento
    from promogest.dao.RigaMovimentoFornitura import RigaMovimentoFornitura
    from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import TestataDocumentoScadenza
    from promogest.dao.ScontoRigaMovimento import ScontoRigaMovimento
    from promogest.dao.ScontoRigaDocumento import ScontoRigaDocumento
    from promogest.dao.NumeroLottoTemp import NumeroLottoTemp
    from promogest.dao.DestinazioneMerce import DestinazioneMerce #v

    from promogest.dao.StoricoDocumento import StoricoDocumento #v

    from promogest.dao.ListinoCategoriaCliente import ListinoCategoriaCliente #v

    from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
    from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
    from promogest.dao.ScontoTestataDocumento import ScontoTestataDocumento
    #from promogest.dao.InformazioniFatturazioneDocumento import t_informazioni_fatturazione_documento

    from promogest.modules.PrimaNota.dao.RigaPrimaNota import RigaPrimaNota
    from promogest.modules.PrimaNota.dao.TestataPrimaNota import TestataPrimaNota
    from promogest.modules.PrimaNota.dao.RigaPrimaNotaTestataDocumentoScadenza import RigaPrimaNotaTestataDocumentoScadenza
    from promogest.dao.RigaRitenutaAcconto import RigaRitenutaAcconto

    from promogest.dao.AnagraficaSecondaria import AnagraficaSecondaria_
    from promogest.modules.GestioneFile.dao.Immagine import ImageFile
    #from promogest.dao.UtenteImmagine import UtenteImmagine
    from promogest.modules.GestioneFile.dao.ArticoloImmagine import ArticoloImmagine
    #from promogest.modules.GestioneFile.dao.SlaFile import SlaFile
    #from promogest.dao.SlaFileImmagine import SlaFileImmagine

    from promogest.modules.GestioneCommesse.dao.StadioCommessa import StadioCommessa
    from promogest.modules.GestioneCommesse.dao.TestataCommessa import TestataCommessa
    from promogest.modules.GestioneCommesse.dao.RigaCommessa import RigaCommessa

def orderedImportVenditaDettaglio():
    orderedImport()
    try:
        from promogest.modules.VenditaDettaglio.dao.Pos import Pos #v
        from promogest.dao.CCardType import CCardType #v
        from promogest.modules.VenditaDettaglio.dao.ScontoScontrino import ScontoScontrino #v
        from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import ScontoRigaScontrino #v
        from promogest.modules.VenditaDettaglio.dao.RigaScontrino import RigaScontrino #v
        from promogest.modules.VenditaDettaglio.dao.TestataScontrino import TestataScontrino #v
        from promogest.modules.VenditaDettaglio.dao.ScontoTestataScontrino import ScontoTestataScontrino #v
        from promogest.modules.VenditaDettaglio.dao.ChiusuraFiscale import ChiusuraFiscale #v
        from promogest.modules.VenditaDettaglio.dao.TestataScontrinoCliente import TestataScontrinoCliente #v
        print "CARICAMENTO/INSERIMENTO TABELLE VENDITA DETTAGLIO  ANDATO BENE"
    except:
        print " DETTAGLIO DA SISTEARE"

    #from data.scontoFornitura import t_sconto_fornitura

    #from data.contattoAnagraficaSecondaria import t_contatto_anagraficasecondaria
def orderedImportWeb():
    #from sqlalchemy import *
    #from sqlalchemy.orm import *
    #try:
    """ RICORDARSI CHE È POSSIBILE CHE CART NON ABBIA ID_CLIENTE E
    STATIC PAGES NON ABBIA PERMALINK, VANNO DROPPATE E RICREATE
    AGGIUNGERE UN CHECK QUI CHE DROPPI E RICREI"""
    from promogest.dao.CategoriaNews import CategoriaNews
    from promogest.dao.News import News #v
    from promogest.dao.StaticPages import StaticPages
    from promogest.dao.Faq import Faq
    from promogest.dao.Cart import Cart
    print "CARICAMENTO/INSERIMENTO TABELLE WEB  ANDATO BENE"
    #except:
        #delete_pickle()
