# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2013 by Promotux
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
from promogest.Environment import delete_pickle
from promogest.dao.DaoUtils import get_columns
from sqlalchemy import *
from sqlalchemy.orm import *

def orderedImport():
    from promogest.dao.Azienda import t_azienda #v
    from promogest.dao.Language import t_language #v
    from promogest.modules.RuoliAzioni.dao.Role import t_role #v
    from promogest.dao.User import t_utente #v
    colonne_utente = colonne = get_columns(t_utente)
    #print "COLONNNNE", colonne_utente,"mailing_list" not in colonne_utente
    if "mailing_list" not in colonne_utente:
        try:
            col = Column('mailing_list', Boolean, default=False)
            col.create(t_utente)
        except:
            delete_pickle()
    if "privacy" not in colonne_utente:
        try:
            col = Column('privacy', Boolean, default=False)
            col.create(t_utente)
        except:
            delete_pickle()
    #from promogest.dao.Regioni import t_regione
    from promogest.modules.RuoliAzioni.dao.Action import t_action  #v
    from promogest.modules.RuoliAzioni.dao.RoleAction import t_roleaction #v
    from promogest.dao.Access import t_access #v
    from promogest.dao.Setting import t_setting #v
    from promogest.dao.Promemoria import t_promemoria #v
    from promogest.dao.Setconf import * #verificare
    from promogest.dao.Pagamento import t_pagamento #v
    from promogest.dao.Operazione import t_operazione #v
    from promogest.dao.TipoAliquotaIva import t_tipo_aliquota_iva #v
    from promogest.dao.daoContatti.TipoRecapito import t_tipo_recapito #v
    from promogest.dao.UnitaBase import t_unita_base #v
    from promogest.dao.StatoArticolo import t_stato_articolo #v
    from promogest.dao.AliquotaIva import t_aliquota_iva #v
    from promogest.dao.CategoriaArticolo import t_categoria_articolo #v
    from promogest.dao.Banca import t_banca #v
    from promogest.dao.BancheAzienda import t_banche_azienda #v
    from promogest.dao.FamigliaArticolo import t_famiglia_articolo #v
    #from promogest.dao.Image import * # ???????????????????
    from promogest.dao.CategoriaCliente import t_categoria_cliente #v
    from promogest.dao.CategoriaFornitore import t_categoria_fornitore #v
    from promogest.dao.Magazzino import t_magazzino  #v

    from promogest.dao.Imballaggio import t_imballaggio #v
    from promogest.dao.Listino import t_listino #v
    from promogest.dao.Articolo import t_articolo #v
    from promogest.dao.CodiceABarreArticolo import t_codice_barre_articolo #v
    from promogest.dao.ListinoArticolo import t_listino_articolo #v
    from promogest.dao.Multiplo import t_multiplo #v

    from promogest.dao.ListinoComplessoListino import t_listino_complesso_listino #v
    from promogest.dao.ListinoComplessoArticoloPrevalente import t_listino_complesso_articolo_prevalente  #v
    from promogest.dao.VariazioneListino import t_variazione_listino #v

    from promogest.dao.daoContatti.RecapitoContatto import t_recapito #v
    from promogest.dao.daoContatti.CategoriaContatto import t_categoria_contatto #v
    from promogest.dao.daoContatti.ContattoCategoriaContatto import t_contatto_categoria_contatto #v
    from promogest.dao.daoContatti.Contatto import t_contatto #v


    from promogest.dao.Stoccaggio import t_stoccaggio #v
    from promogest.dao.PersonaGiuridica import t_persona_giuridica #v
    from promogest.dao.PersonaGiuridicaPersonaGiuridica import t_personagiuridica_personagiuridica #v



    from promogest.dao.Vettore import t_vettore #v
    from promogest.dao.ListinoMagazzino import t_listino_magazzino #v

    from promogest.dao.Cliente import t_cliente #v
    from promogest.dao.Fornitore import t_fornitore #v
    from promogest.dao.Fornitura import t_fornitura  #v
    from promogest.dao.daoAgenti.Agente import t_agente #v
    from promogest.dao.ClienteCategoriaCliente import t_cliente_categoria_cliente #v
    from promogest.dao.ClienteVariazioneListino import t_cliente_variazione_listino #v
    from promogest.dao.Sconto import t_sconto
    from promogest.dao.daoContatti.RecapitoContatto import t_recapito
    from promogest.dao.daoContatti.ContattoCliente import t_contatto_cliente
    from promogest.dao.daoContatti.ContattoFornitore import t_contatto_fornitore
    from promogest.dao.daoContatti.ContattoAzienda import t_contatto_azienda
    from promogest.dao.daoContatti.ContattoMagazzino import t_contatto_magazzino
    from promogest.dao.daoContatti.ContattoCategoriaContatto import t_contatto_categoria_contatto

    from promogest.dao.Riga import t_riga
    from promogest.dao.AccountEmail import t_account_email

    from promogest.dao.TestataDocumento import t_testata_documento #v
    from promogest.dao.TestataMovimento import t_testata_movimento   #v
    from promogest.dao.RigaDocumento import t_riga_documento
    from promogest.dao.RigaMovimento import t_riga_movimento #v
    from promogest.dao.RigaMovimentoFornitura import t_riga_movimento_fornitura
    from promogest.modules.Pagamenti.dao.TestataDocumentoScadenza import t_testata_documento_scadenza
    from promogest.dao.ScontoRigaMovimento import t_sconto_riga_movimento
    from promogest.dao.ScontoRigaDocumento import t_sconto_riga_documento
    from promogest.dao.NumeroLottoTemp import t_numero_lotto_temp
    from promogest.dao.DestinazioneMerce import t_destinazione_merce #v

    from promogest.dao.ListinoCategoriaCliente import t_listino_categoria_cliente #v

    from promogest.dao.ScontoVenditaDettaglio import t_sconti_vendita_dettaglio
    from promogest.dao.ScontoVenditaIngrosso import t_sconti_vendita_ingrosso
    from promogest.dao.ScontoTestataDocumento import t_sconto_testata_documento
    from promogest.dao.InformazioniFatturazioneDocumento import t_informazioni_fatturazione_documento

    from promogest.modules.PrimaNota.dao.RigaPrimaNota import t_riga_prima_nota
    from promogest.modules.PrimaNota.dao.TestataPrimaNota import t_testata_prima_nota
    from promogest.modules.PrimaNota.dao.RigaPrimaNotaTestataDocumentoScadenza import t_riga_primanota_testata_documento_scadenza
    from promogest.dao.RigaRitenutaAcconto import t_ritenuta_acconto_riga

    from promogest.dao.AnagraficaSecondaria import t_anagrafica_secondaria
    from promogest.modules.GestioneFile.dao.Immagine import t_immagine
    from promogest.dao.UtenteImmagine import t_utente_immagine
    from promogest.modules.GestioneFile.dao.ArticoloImmagine import t_articolo_immagine
    from promogest.modules.GestioneFile.dao.SlaFile import t_sla_file
    from promogest.dao.SlaFileImmagine import t_slafile_immagine

    from promogest.modules.GestioneCommesse.dao.StadioCommessa import t_stadio_commessa
    from promogest.modules.GestioneCommesse.dao.TestataCommessa import t_testata_commessa
    from promogest.modules.GestioneCommesse.dao.RigaCommessa import t_riga_commessa

def orderedImportVenditaDettaglio():
#try:
    from promogest.modules.VenditaDettaglio.dao.Pos import t_pos #v
    from promogest.modules.VenditaDettaglio.dao.ScontoScontrino import t_sconto_scontrino #v
    from promogest.dao.CCardType import t_credit_card_type #v
    from promogest.modules.VenditaDettaglio.dao.RigaScontrino import t_riga_scontrino #v
    from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import t_sconto_riga_scontrino #v
    from promogest.modules.VenditaDettaglio.dao.TestataScontrino import t_testata_scontrino #v
    from promogest.modules.VenditaDettaglio.dao.ScontoTestataScontrino import t_sconto_testata_scontrino #v
    from promogest.modules.VenditaDettaglio.dao.ChiusuraFiscale import t_chiusura_fiscale #v
    from promogest.modules.VenditaDettaglio.dao.TestataScontrinoCliente import t_testata_scontrino_cliente #v

    print "CARICAMENTO/INSERIMENTO TABELLE VENDITA DETTAGLIO  ANDATO BENE"
#except:
    #print " DETTAGLIO DA SISTEARE"

    #from data.scontoFornitura import t_sconto_fornitura

    #from data.contattoAnagraficaSecondaria import t_contatto_anagraficasecondaria
def orderedImportWeb():
    from promogest.dao.DaoUtils import get_columns
    from sqlalchemy import *
    from sqlalchemy.orm import *
#try:
    """ RICORDARSI CHE È POSSIBILE CHE CART NON ABBIA ID_CLIENTE E
    STATIC PAGES NON ABBIA PERMALINK, VANNO DROPPATE E RICREATE
    AGGIUNGERE UN CHECK QUI CHE DROPPI E RICREI"""
    from promogest.dao.NewsCategory import t_news_category
    from promogest.dao.News import t_news #v
    from promogest.dao.StaticPages import t_static_page
    colonne_st_pages = colonne = get_columns(t_static_page)
    if "permalink" not in colonne_st_pages:
        col = Column('permalink', Integer)
        col.create(t_static_page)
    from promogest.dao.Faq import t_faq
    from promogest.dao.Cart import t_cart
    colonne_cart = colonne = get_columns(t_cart)
    if "id_cliente" not in colonne_cart:
        col = Column('id_cliente', Integer)
        col.create(t_cart)
    print "CARICAMENTO/INSERIMENTO TABELLE WEB  ANDATO BENE"
