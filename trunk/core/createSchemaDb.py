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


from promogest.preEnv import *
from promogest.Environment import *
from sqlalchemy.schema import CreateSchema


def buildAll():
    delete_pickle()
    if tipo_eng == "postgresql":
        try:
            engine.execute(CreateSchema(buildSchema))
        except:
            print "CREAZIONE SCHEMA", buildSchema, "NON RIUSCITO O GIA ESISTENTE"

    if tipo_eng == "postgresql":
        try:
            engine.execute(CreateSchema("promogest2"))
        except:
            print "CREAZIONE SCHEMA promogest2 NON RIUSCITO O GIA ESISTENTE"

    try:
        from data.azienda import t_azienda
        from data.language import t_language
        from data.role import t_role
        from data.utente import t_utente
        from data.regione import t_regione
        from data.action import t_action
        from data.roleAction import t_roleaction
        from data.access import t_access
        from data.setting import t_setting
        from data.promemoria import t_promemoria
        from data.setconf import t_setconf

        from data.pagamento import t_pagamento
        from data.operazione import t_operazione
        from data.tipoAliquotaiva import t_tipo_aliquota_iva
        from data.unitaBase import t_unita_base
        from data.aliquotaIva import t_aliquota_iva
        from data.categoria_articolo import t_categoria_articolo
        from data.banca import t_banca
        from data.bancheAzienda import t_banche_azienda
        from data.statoArticolo import t_stato_articolo
        from data.famigliaArticolo import t_famiglia_articolo
        from data.image import t_image
        from data.imballaggio import t_imballaggio
        from data.listino import t_listino
        from data.articolo import t_articolo
        from data.codiceBarreArticolo import t_codice_barre_articolo
        from data.articoloKit import t_articolo_kit
        from data.listinoArticolo import t_listino_articolo
        from data.multiplo import t_multiplo
        from data.listinoComplessoListino import t_listino_complesso_listino
        from data.listinoComplessoArticoloPrevalente import t_listino_complesso_articolo_prevalente
        from data.variazioneListino import t_variazione_listino

        from data.tiporecapito import t_tipo_recapito
        from data.categoriaCliente import t_categoria_cliente
        from data.categoriaFornitore import t_categoria_fornitore
        from data.categoriaContatto import t_categoria_contatto

        from data.magazzino import t_magazzino
        from data.stoccaggio import t_stoccaggio
        from data.personaGiuridica import t_persona_giuridica
        from data.personaGiuridicaPersonaGiuridica import t_personagiuridica_personagiuridica
        from data.vettore import t_vettore
        from data.listinoMagazzino import t_listino_magazzino

        from data.cliente import t_cliente
        from data.fornitore import t_fornitore
        from data.agente import t_agente
        from data.clienteCategoriaCliente import t_cliente_categoria_cliente
        from data.clienteVariazioneListino import t_cliente_variazione_listino

        from data.contatto import t_contatto
        from data.recapito import t_recapito
        from data.contattoCliente import t_contatto_cliente
        from data.contattoFornitore import t_contatto_fornitore
        from data.contattoAzienda import t_contatto_azienda
        from data.contattoMagazzino import t_contatto_magazzino
        from data.destinazioneMerce import t_destinazione_merce
        from data.contattoCategoriaContatto import t_contatto_categoria_contatto
        from data.listinoCategoriaCliente import t_listino_categoria_cliente

        from data.riga import t_riga
        from data.testataDocumento import t_testata_documento
        from data.testataMovimento import t_testata_movimento
        from data.rigaMovimento import t_riga_movimento
        from data.rigaDocumento import t_riga_documento
        from data.informazioniContabiliDocumento import t_informazioni_contabili_documento
        from data.informazioniFatturazioneDocumento import t_informazioni_fatturazione_documento
        from data.testataDocumentoScadenza import t_testata_documento_scadenza

        from data.fornitura import t_fornitura
        from data.sconto import t_sconto
        from data.scontoFornitura import t_sconto_fornitura
        from data.scontoRigaMovimento import t_sconto_riga_movimento
        from data.scontoRigaDocumento import t_sconto_riga_documento
        from data.scontoTestataDocumento import t_sconto_testata_documento
        from data.scontiVenditaDettaglio import t_sconti_vendita_dettaglio
        from data.scontiVenditaIngrosso import t_sconti_vendita_ingrosso
        from data.rigaMovimentoFornitura import t_riga_movimento_fornitura
        from data.rigaRitenutaAcconto import t_ritenuta_acconto_riga

        from data.inventario import t_inventario
        from data.anagraficaSecondaria import t_anagrafica_secondaria
        from data.contattoAnagraficaSecondaria import t_contatto_anagraficasecondaria

        from data.stadio_commessa import t_stadio_commessa
        from data.testataCommessa import t_testata_commessa
        from data.rigaCommessa import t_riga_commessa

        from data.immagine import t_immagine
        from data.utenteImmagine import t_utente_immagine
        from data.articoloImmagine import t_articolo_immagine
        from data.slafile import t_sla_file
        from data.slafileImmagine import t_slafile_immagine
        from data.numerolottotemp import t_numero_lotto_temp

        from data.testataPrimaNota import t_testata_prima_nota
        from data.rigaPrimaNota import t_riga_prima_nota
        from data.rigaPrimaNotaTestataDocumentoScadenza import t_riga_primanota_testata_documento_scadenza
        print " FINITA L'AGGIUNTA DELLE TABELLE"
    except Exception as e:
        print "DELLA CREAZIONE TABELLE QUALCOSA NON E' ANDATO BENE", e
