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

from promogest.dao.Azienda import t_azienda, Azienda
from promogest.dao.Language import *
from promogest.modules.RuoliAzioni.dao.Role import *
from promogest.dao.User import *
from promogest.dao.Regioni import *
from promogest.modules.RuoliAzioni.dao.Action import *
from promogest.modules.RuoliAzioni.dao.RoleAction import *
from promogest.dao.Access import *
from promogest.dao.Setting import *
from promogest.dao.Promemoria import *
from promogest.dao.Setconf import *
from promogest.dao.Pagamento import *
from promogest.dao.Operazione import *
from promogest.dao.TipoAliquotaIva import *
from promogest.dao.daoContatti.TipoRecapito import *
from promogest.dao.UnitaBase import *
from promogest.dao.StatoArticolo import *
from promogest.dao.AliquotaIva import *
from promogest.dao.CategoriaArticolo import *
from promogest.dao.Banca import t_banca, Banca
from promogest.dao.BancheAzienda import t_banche_azienda, BancheAzienda
from promogest.dao.FamigliaArticolo import *
#from promogest.dao.Image import *  ???????????????????
from promogest.dao.Imballaggio import *
from promogest.dao.Listino import *
from promogest.dao.Articolo import *
from promogest.dao.CodiceABarreArticolo import *
from promogest.dao.ListinoArticolo import *
from promogest.dao.Multiplo import *

from promogest.dao.ListinoComplessoListino import *
from promogest.dao.ListinoComplessoArticoloPrevalente import *
from promogest.dao.VariazioneListino import *


from promogest.dao.daoContatti.RecapitoContatto import *
from promogest.dao.daoContatti.CategoriaContatto import *
from promogest.dao.daoContatti.ContattoCategoriaContatto import *
from promogest.dao.daoContatti.Contatto import *

from promogest.dao.Magazzino import *
from promogest.dao.Stoccaggio import *
from promogest.dao.PersonaGiuridica import *
from promogest.dao.PersonaGiuridicaPersonaGiuridica import *

from promogest.dao.CategoriaCliente import *
from promogest.dao.CategoriaFornitore import *

from promogest.dao.Vettore import t_vettore
from promogest.dao.ListinoMagazzino import t_listino_magazzino

from promogest.dao.Cliente import t_cliente, Cliente
from promogest.dao.Fornitore import t_fornitore, Fornitore
from promogest.dao.daoAgenti.Agente import t_agente, Agente
from promogest.dao.ClienteCategoriaCliente import t_cliente_categoria_cliente, ClienteCategoriaCliente
from promogest.dao.ClienteVariazioneListino import t_cliente_variazione_listino

from promogest.dao.daoContatti.Contatto import t_contatto
from promogest.dao.daoContatti.RecapitoContatto import t_recapito
from promogest.dao.daoContatti.ContattoCliente import t_contatto_cliente
from promogest.dao.daoContatti.ContattoFornitore import t_contatto_fornitore
from promogest.dao.daoContatti.ContattoAzienda import t_contatto_azienda

from promogest.dao.Riga import t_riga
try:

    from promogest.modules.VenditaDettaglio.dao.TestataScontrino import *
    from promogest.modules.VenditaDettaglio.dao.RigaScontrino import *
    from promogest.modules.VenditaDettaglio.dao.ScontoScontrino import *
    from promogest.modules.VenditaDettaglio.dao.ScontoRigaScontrino import *
except:
    print "IMPORT VENDITA DETTAGLIO DA RIVEDERE"

def orderedImport():
    return


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
