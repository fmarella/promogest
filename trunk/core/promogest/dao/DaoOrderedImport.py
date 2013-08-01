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
#from promogest.Environment import *

def orderedImport():
    from promogest.dao.Azienda import t_azienda, Azienda
    from promogest.dao.Language import t_language #v
    from promogest.modules.RuoliAzioni.dao.Role import t_role #v
    from promogest.dao.User import t_utente #v
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
    #from promogest.dao.Image import *  ???????????????????
    from promogest.dao.Imballaggio import t_imballaggio #v
    from promogest.dao.Listino import t_listino #v
    from promogest.dao.Articolo import t_articolo #v
    from promogest.dao.CodiceABarreArticolo import t_codice_barre_articolo #v
    from promogest.dao.ListinoArticolo import t_listino_articolo #v
    from promogest.dao.Multiplo import t_multiplo #v

    from promogest.dao.ListinoComplessoListino import t_listino_complesso_listino
    from promogest.dao.ListinoComplessoArticoloPrevalente import t_listino_complesso_articolo_prevalente
    from promogest.dao.VariazioneListino import t_variazione_listino


    from promogest.dao.daoContatti.RecapitoContatto import t_recapito #v
    from promogest.dao.daoContatti.CategoriaContatto import t_categoria_contatto #v
    from promogest.dao.daoContatti.ContattoCategoriaContatto import t_contatto_categoria_contatto #v
    from promogest.dao.daoContatti.Contatto import t_contatto #v

    from promogest.dao.Magazzino import t_magazzino  #v
    from promogest.dao.Stoccaggio import t_stoccaggio #v
    from promogest.dao.PersonaGiuridica import t_persona_giuridica #v
    from promogest.dao.PersonaGiuridicaPersonaGiuridica import t_personagiuridica_personagiuridica #v

    from promogest.dao.CategoriaCliente import t_categoria_cliente #v
    from promogest.dao.CategoriaFornitore import t_categoria_fornitore #v

    from promogest.dao.Vettore import t_vettore #v
    from promogest.dao.ListinoMagazzino import t_listino_magazzino #v

    from promogest.dao.Cliente import t_cliente #v
    from promogest.dao.Fornitore import t_fornitore #v
    from promogest.dao.daoAgenti.Agente import t_agente #v
    from promogest.dao.ClienteCategoriaCliente import t_cliente_categoria_cliente #v
    from promogest.dao.ClienteVariazioneListino import t_cliente_variazione_listino #v

    from promogest.dao.daoContatti.RecapitoContatto import t_recapito
    from promogest.dao.daoContatti.ContattoCliente import t_contatto_cliente
    from promogest.dao.daoContatti.ContattoFornitore import t_contatto_fornitore
    from promogest.dao.daoContatti.ContattoAzienda import t_contatto_azienda

    from promogest.dao.Riga import t_riga

#def orderedImportVenditaDettaglio():
try:
    from promogest.modules.VenditaDettaglio.dao.TestataScontrino import *
    from promogest.modules.VenditaDettaglio.dao.RigaScontrino import *
    from promogest.modules.VenditaDettaglio.dao.ScontoScontrino import *
    from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import *
    from promogest.modules.VenditaDettaglio.dao.ScontoTestataScontrino import *
    from promogest.modules.VenditaDettaglio.dao.ChiusuraFiscale import *
    from promogest.modules.VenditaDettaglio.dao.TestataScontrinoCliente import *
    from promogest.modules.VenditaDettaglio.dao.Pos import *
except:
    print " DETTAGLIO DA SISTEARE"


    #from data.contattoMagazzino import t_contatto_magazzino
    #from data.destinazioneMerce import t_destinazione_merce
    #from data.contattoCategoriaContatto import t_contatto_categoria_contatto
    #from data.listinoCategoriaCliente import t_listino_categoria_cliente

    #from data.testataDocumento import t_testata_documento
    #from data.testataMovimento import t_testata_movimento
    #from data.rigaMovimento import t_riga_movimento
    #from data.rigaDocumento import t_riga_documento
    #from data.informazioniContabiliDocumento import t_informazioni_contabili_documento
    #from data.informazioniFatturazioneDocumento import t_informazioni_fatturazione_documento
    #from data.testataDocumentoScadenza import t_testata_documento_scadenza

    #from data.fornitura import t_fornitura
    #from data.sconto import t_sconto
    #from data.scontoFornitura import t_sconto_fornitura
    #from data.scontoRigaMovimento import t_sconto_riga_movimento
    #from data.scontoRigaDocumento import t_sconto_riga_documento
    #from data.scontoTestataDocumento import t_sconto_testata_documento
    #from data.scontiVenditaDettaglio import t_sconti_vendita_dettaglio
    #from data.scontiVenditaIngrosso import t_sconti_vendita_ingrosso
    #from data.rigaMovimentoFornitura import t_riga_movimento_fornitura
    #from data.rigaRitenutaAcconto import t_ritenuta_acconto_riga

    #from data.inventario import t_inventario
    #from data.anagraficaSecondaria import t_anagrafica_secondaria
    #from data.contattoAnagraficaSecondaria import t_contatto_anagraficasecondaria

    #from data.stadio_commessa import t_stadio_commessa
    #from data.testataCommessa import t_testata_commessa
    #from data.rigaCommessa import t_riga_commessa

    #from data.immagine import t_immagine
    #from data.utenteImmagine import t_utente_immagine
    #from data.articoloImmagine import t_articolo_immagine
    #from data.slafile import t_sla_file
    #from data.slafileImmagine import t_slafile_immagine
    #from data.numerolottotemp import t_numero_lotto_temp

    #from data.testataPrimaNota import t_testata_prima_nota
    #from data.rigaPrimaNota import t_riga_prima_nota
    #from data.rigaPrimaNotaTestataDocumentoScadenza import t_riga_primanota_testata_documento_scadenza
