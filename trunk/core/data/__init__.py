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


#                               from schemi.categoria_articolo import CategoriaArticoloDb
#                               from schemi.banca import BancaDb
#                               from schemi.family import FamilyArticleDb
#                               from schemi.aliquotaIva import AliquotaIvaDb
#                               from schemi.listino import ListinoDb
#                               from schemi.listinoArticolo import ListinoArticoloDb
#                               from schemi.article import ArticleDb
#                               from schemi.agente import AgenteDb
#                               from schemi.unitaBase import UnitaBaseDb
#                               from schemi.testataMovimento import TestataMovimentoDb
#                               from schemi.testataDocumento import TestataDocumentoDb
#                               from schemi.rigaMovimento import RigaMovimentoDb
#                               from schemi.riga import RigaDb
#                               from schemi.cliente import ClienteDb
#                               from schemi.recapito import RecapitoDb
#                               from schemi.personaGiuridica import PersonaGiuridicaDb
#                               from schemi.operazione import OperazioneDb
#                               from schemi.statoArticolo import StatoArticoloDb
#                               from schemi.tipoAliquotaiva import TipoAliquotaIvaDb
#                               from schemi.tiporecapito import TipoRecapitoDb
#                               from schemi.contatto import ContattoDb
#                               from schemi.company import CompanyDb
#                               from schemi.contattoCliente import ContattoClienteDb
#                               from schemi.contattoAzienda import ContattoAziendaDb
#                               from schemi.contattoFornitore import ContattoFornitoreDb
#                               from schemi.contattoMagazzino import ContattoMagazzinoDb
#                               from schemi.categoriaCliente import CategoriaClienteDb
#                               from schemi.categoriaContatto import CategoriaContattoDb
#                               from schemi.clienteCategoriaCliente import ClienteCategoriaClienteDb
#                               from schemi.codiceBarreArticolo import CodiceBarreArticoloDb
#                               from schemi.contattoCategoriaContatto import ContattoCategoriaContattoDb
#                               from schemi.destinazioneMerce import  DestinazioneMerceDb
#                               from schemi.listinoCategoriaCliente import ListinoCategoriaClienteDb
#                               from schemi.listinoMagazzino import ListinoMagazzinoDb
#                               from schemi.magazzino import MagazzinoDb
#                               from schemi.informazioniContabiliDocumento import InformazioniContabiliDocumentoDb
#                               from schemi.informazioniFatturazioneDocumento import InformazioniFatturazioneDocumentoDb
#                               from schemi.multiplo import MultiploDb
#                               from schemi.pagamento import PagamentoDb
#                               from schemi.sconto import ScontoDb
#                               from schemi.categoriaFornitore import CategoriaFornitoreDb
#                               from schemi.fornitore import FornitoreDb
#                               from schemi.fornitura import FornituraDb
#                               from schemi.scontoFornitura import ScontoFornituraDb
#                               from schemi.scontoRigaMovimento import ScontoRigaMovimentoDb
#                               from schemi.vettore import VettoreDb
#                               from schemi.access import AccessDb
#                               from schemi.image import ImageDb
#                               from schemi.imballaggio import ImballaggioDb
#                               from schemi.action import ActionDb
#                               from schemi.user import UserDb
#                               from schemi.role import RoleDb
#                               from schemi.roleAction import RoleActionDb
################################from schemi.cart import CartDb
################################from schemi.pages import PagesDb
################################from schemi.scontoWeb import ScontoWebDb
################################from schemi.staticMenu import StaticMenuDb
################################from schemi.articoloAssociato import ArticoloAssociatoDb
#                               from schemi.language import LanguageDb
#                               from schemi.setting import SettingDb
################################from schemi.feed import FeedDb
################################from schemi.spesa import SpesaDb
#                               from schemi.stoccaggio import StoccaggioDb
#                               from schemi.inventario import InventarioDb
#                               from schemi.promemoria import PromemoriaDb
#                               from schemi.rigaDocumento import RigaDocumentoDb
#                               from schemi.scontoTestataDocumento import ScontoTestataDocumentoDb
#                               from schemi.testataDocumentoScadenza import TestataDocumentoScadenzaDb
#                               from schemi.scontiVenditaDettaglio import ScontiVenditaDettaglioDb
#                               from schemi.scontiVenditaIngrosso import ScontiVenditaIngrossoDb
#                               from schemi.listinoComplessoListino import ListinoComplessoListinoDb
#                               from schemi.listinoComplessoArticoloPrevalente import ListinoComplessoArticoloPrevalenteDb
#from schemi.appLog import AppLogDb
#from schemi.chiaviPrimarieLog import ChiaviPrimarieLogDb
#                                from schemi.scontoRigaDocumento import ScontoRigaDocumentoDb
#################################from schemi.scontoRigaScontrino import ScontoRigaScontrinoDb
#################################from schemi.rigaScontrino import RigaScontrinoDb
#################################from schemi.testataScontrino import TestataScontrinoDb
#################################from schemi.chiusuraFiscale import ChiusuraFiscaleDb
#################################from schemi.stadio_commessa import StadioCommessaDb
#################################from schemi.testataCommessa import TestataCommessaDb
#################################from schemi.rigaCommessa import RigaCommessaDb
