# -*- coding: utf-8 -*-

# Promogest
#
# Copyright (C) 2007 by Promotux Informatica - http://www.promotux.it/
# Author:  Marco Pinna "Dr astico" <zoccolodignu@gmail.com>
# Author:  Francesco Meloni  "Vete" <francesco@promotux.it.com>

import decimal
from decimal import *
import gtk
from datetime import datetime
import xml.etree.cElementTree as ElementTree
from promogest import Environment
from promogest.ui.GladeWidget import GladeWidget
from promogest.dao.Articolo import Articolo
from promogest.dao.AliquotaIva import AliquotaIva
from promogest.dao.CodiceABarreArticolo import CodiceABarreArticolo
from promogest.dao.FamigliaArticolo import FamigliaArticolo
from promogest.dao.CategoriaArticolo import CategoriaArticolo
from promogest.dao.Fornitura import Fornitura
from promogest.dao.Listino import Listino
from promogest.dao.ListinoArticolo import ListinoArticolo
from promogest.dao.UnitaBase import UnitaBase
from promogest.dao.ScontoVenditaDettaglio import ScontoVenditaDettaglio
from promogest.dao.ScontoVenditaIngrosso import ScontoVenditaIngrosso
import promogest.ui.AnagraficaListini
import promogest.ui.Main
from promogest.ui.Main import *
from promogest.ui.AnagraficaListini import AnagraficaListini
from promogest.ui.AnagraficaAliquoteIva import AnagraficaAliquoteIva
from promogest.ui.AnagraficaCategorieArticoli import AnagraficaCategorieArticoli
from promogest.ui.AnagraficaFamiglieArticoli import AnagraficaFamiglieArticoli
from promogest.ui.AnagraficaFornitori import AnagraficaFornitori
from promogest.ui.utils import *
from promogest.ui.utilsCombobox import fillModelCombobox,fillComboboxListini
import promogest.ui.Login
#from ImportPriceListPreview import ImportPreview
from fieldsDict import *
if "PromoWear" in Environment.modulesList:
    from promogest.modules.PromoWear.dao.AnnoAbbigliamento import AnnoAbbigliamento
    from promogest.modules.PromoWear.dao.GenereAbbigliamento import GenereAbbigliamento
    from promogest.modules.PromoWear.dao.StagioneAbbigliamento import StagioneAbbigliamento
    from promogest.modules.PromoWear.dao.GruppoTaglia import GruppoTaglia
    from promogest.modules.PromoWear.dao.Modello import Modello
    from promogest.modules.PromoWear.dao.Taglia import Taglia
    from promogest.modules.PromoWear.dao.Colore import Colore

class ProductFromCsv(object):
    """Takes a product from a generic price list and "translates" it in a
    promogest-compatible dao product, ListinoArticolo and Fornitura"""

    def __init__(self, product, PLModel, promoPriceList, idfornitore,dataListino):
        self.PLModel = PLModel
        self.product = product
        self.promoPriceList = promoPriceList or None
        self.fornitore = idfornitore
        self.dataListino = dataListino
        self.daoArticolo = None
        if self.promoPriceList:
            liss = Listino().select(idListino=self.promoPriceList,batchSize=None)
            if liss:
                self.price_list_id = liss[0].id
            del self.promoPriceList
        self.defaults = self.PLModel._defaultAttributes

    def save(self):
        """Gets the existing Dao"""
        self.articolopromoWear = ""
        for key in possibleFieldsDict.keys():
            if key not in self.product.keys():
                setattr(self, possibleFieldsDict[key], None)
            else:
                setattr(self, possibleFieldsDict[key], self.product[key])
        if self.codice_articolo:
            try:
                self.daoArticolo = Articolo().select(codiceEM=self.codice_articolo)[0]
            except:
                pass

        elif self.codice_barre_articolo:
            daoCodiceABarre = CodiceABarreArticolo().select(codiceEM=self.codice_barre_articolo)
            if daoCodiceABarre:
                self.daoArticolo = Articolo().getRecord(id=daoCodiceABarre[0].id_articolo)

        elif self.codice_fornitore:
            daoFornitura =Fornitura().select(codiceArticoloFornitoreEM=self.codice_fornitore)
            if len(daoFornitura) == 1:
                self.daoArticolo = Articolo().getRecord(id=daoFornitura[0].id_articolo)
        else:
            self.daoArticolo = Articolo()
        if "PromoWear" in Environment.modulesList:
            if self.codice_padre and self.codice_articolo:
                print "ARTICOLO PADRE"
                self.articolopromoWear = "father"
                self.addTagliaColoreData(self.daoArticolo[0])
            elif self.codice_padre and not self.codice_articolo:
                print "ARTICOLO FIGLIO"
                self.articolopromoWear = "son"
                self.daoArticolo = Articolo().select(codiceEM=self.codice_articolo)
                if not self.daoArticolo:
                    print "ERROREEEEEEEEE  non può essere caricato un figlio senza il padre"
                else:
                    self.addTagliaColoreData(self.daoArticolo[0])
            elif not self.codice_padre and self.codice_articolo:
                print "ARTICOLO NORMALE"
                self.articolopromoWear = ""
        self.fillDaos()

    def addTagliaColoreData(self, articolo):
        """
        modello, genere, colore, gruppo taglia, taglia, stagione, anno
        """
        artTC = ArticoloTagliaColore().select(idArticoloPadre = articolo.id)
        if artTC:
            artTC = artTC[0]
        else:
            artTC = ArticoloTagliaColore()

        #modello
        if self.modello:
            mode = Modello().select(denominazione = self.modello)
            if mode:
                mode = mode[0]
                artTC.id_modello = mode.id
            else:
                mode = Modello()
                mode.denominazione_breve = self.modello
                mode.denominazione = self.modello
                mode.persist()
                artTC.id_modello = mode.id
        elif not self.modello:
            artTC.id_modello = articolo.id_modello

        #anno
        if self.anno:
            anno = AnnoAbbigliamento().select(denominazione = self.anno)
            if anno:
                anno = anno[0]
                artTC.id_anno = anno.id
            else:
                anno = AnnoAbbigliamento()
                anno.denominazione = self.anno
                anno.persist()
                artTC.id_anno = anno.id
        elif not self.anno:
            artTC.id_annno = articolo.id_anno



    def fillDaos(self):
        """fillDaos method fills all Dao related to daoArticolo"""
        self.codice_articolo = str(self.codice_articolo)
        if self.codice_articolo is None or  self.codice_articolo == "None":
            self.codice_articolo = promogest.dao.Articolo.getNuovoCodiceArticolo()
        self.daoArticolo.codice = self.codice_articolo

        self.denominazione_articolo = str(self.denominazione_articolo)
        self.daoArticolo.denominazione = self.denominazione_articolo

        #families
        id_famiglia = None
        if self.famiglia_articolo is None:
            self.famiglia_articolo_id = int(self.defaults['Famiglia'])
            self.famiglia_articolo = FamigliaArticolo().getRecord(id=self.famiglia_articolo_id)
            id_famiglia = self.famiglia_articolo.id

        else:
            self._families = FamigliaArticolo().select(batchSize=None)
            code_list = []
            for f in self._families:
                code_list.append(f.codice)
                if self.famiglia_articolo in  (f.denominazione_breve, f.denominazione, f.codice, f.id):
                    id_famiglia = f.id

                    break
            if  id_famiglia is None:
                family_code = self.famiglia_articolo[:4]
                if len(self._families) > 0:
                    ind = 0
                    for code in code_list:
                        if family_code == code[:4]:
                            ind +=1
                    family_code = family_code+'/'+str(ind)

                daoFamiglia = FamigliaArticolo()
                daoFamiglia.codice = family_code
                daoFamiglia.denominazione_breve = self.famiglia_articolo[:10]
                daoFamiglia.denominazione = self.famiglia_articolo
                daoFamiglia.id_padre = None
                daoFamiglia.persist()
                id_famiglia = daoFamiglia.id
                self._families.append(daoFamiglia)
        self.daoArticolo.id_famiglia_articolo = id_famiglia

        #categories
        id_categoria = None
        if self.categoria_articolo is None:
            self.categoria_articolo_id = self.defaults['Categoria']
            self.categoria_articolo = CategoriaArticolo().getRecord(id=self.categoria_articolo_id)
            id_categoria = self.categoria_articolo.id
        else:
            self._categories = CategoriaArticolo().select(batchSize=None)
            category_list = []
            for c in self._categories:
                category_list.append(c.denominazione_breve)
                if self.categoria_articolo in (c.denominazione, c.denominazione_breve):
                    id_categoria = c.id
                    break
            if id_categoria == None:
                category_short_name = self.categoria_articolo[:7]
                if len(self._categories) > 0:
                    ind = 0
                    for category in category_list:
                        if category_short_name == category[:7]:
                            ind +=1
                    category_short_name = category_short_name+'/'+str(ind)
                daoCategoria = CategoriaArticolo()
                daoCategoria.denominazione_breve = category_short_name
                daoCategoria.denominazione = self.categoria_articolo
                daoCategoria.persist()
                id_categoria = daoCategoria.id
                self._categories.append(daoCategoria)
        self.daoArticolo.id_categoria_articolo = id_categoria


        #IVA
        id_aliquota_iva = None
        if self.aliquota_iva is None:
            self.aliquota_iva_id = self.defaults['Aliquota iva']
            self.aliquota_iva = AliquotaIva().getRecord(id=self.aliquota_iva_id)
            id_aliquota_iva = self.aliquota_iva.id
        else:
            self._vats = AliquotaIva().select(batchSize=None)
            for v in self._vats:
                if self.aliquota_iva.lower() in (v.denominazione_breve.lower(),v.denominazione.lower()) or\
                            int(str(self.aliquota_iva).replace('%','')) == int(v.percentuale):
                    id_aliquota_iva = v.id
                    break
            if id_aliquota_iva is None:
                self.aliquota_iva = str(self.aliquota_iva).replace('%','')
                daoAliquotaIva = AliquotaIva()
                daoAliquotaIva.denominazione = 'ALIQUOTA '+ self.aliquota_iva +'%'
                daoAliquotaIva.denominazione_breve = self.aliquota_iva + '%'
                daoAliquotaIva.id_tipo = 1
                daoAliquotaIva.percentuale = Decimal(self.aliquota_iva)
                daoAliquotaIva.persist()
                id_aliquota_iva = daoAliquotaIva.id
                self._vats.append(daoAliquotaIva)
        self.daoArticolo.id_aliquota_iva = id_aliquota_iva
        

        #base units
        id_unita_base = None
        if  self.unita_base is None:
            self.unita_base_id = self.defaults['Unita base']
            #FIXME: promogest2 ----proviamo
            # La storedProcedure UnitaBaseGet NON esiste e la chiamta Dao qui sotto fallisce con un errore!!!
            self.unita_base = UnitaBase().getRecord(id=self.unita_base_id)
            id_unita_base = self.unita_base_id
        else:
            unis = UnitaBase().select(batchSize=None)
            for u in unis:
                if self.unita_base.lower() in (u.denominazione.lower(),u.denominazione_breve.lower()):
                    id_unita_base = u.id
                    break
            if id_unita_base is None:
                self.unita_base = UnitaBase().select(denominazione='Pezzi',
                                                                    batchSize=None)
                id_unita_base = self.unita_base.id
        self.daoArticolo.id_unita_base = id_unita_base
        self.daoArticolo.produttore = self.produttore or ''
        self.daoArticolo.cancellato = False
        self.daoArticolo.sospeso = False
        #Environment.params['session'].add(self.daoArticolo)
        #Environment.params['session'].commit()
        self.daoArticolo.persist()

        product_id = self.daoArticolo.id

        #barcode
        if self.codice_barre_articolo is not None:
            self.codice_barre_articolo = str(self.codice_barre_articolo).strip()
            try:
                oldCodeBar= CodiceABarreArticolo().select(idArticolo=product_id)
                if oldCodeBar:
                    for codes in oldCodeBar:
                        codes.primario = False
                        codes.persist()
            except:
                pass
            barCode = CodiceABarreArticolo().select(codiceEM=self.codice_barre_articolo,
                                                                                batchSize=None)
            if len(barCode) > 0:
                daoBarCode = CodiceABarreArticolo().getRecord(id=barCode[0].id)
                daoBarCode.id_articolo = product_id
                daoBarCode.primario = True
                daoBarCode.persist()
            else:
                daoBarCode = CodiceABarreArticolo()
                daoBarCode.id_articolo = product_id
                daoBarCode.codice = self.codice_barre_articolo
                daoBarCode.primario = True
                daoBarCode.persist()

        #price-list--> product
        decimalSymbol = self.PLModel._decimalSymbol
        if (self.prezzo_vendita_non_ivato is not None or self.prezzo_acquisto_non_ivato is not None or self.prezzo_acquisto_ivato is not None or
            self.prezzo_vendita_ivato is not None):
            try:
                daoPriceListProduct = ListinoArticolo().select(idListino=self.price_list_id,
                                                                    idArticolo=product_id,
                                                                    batchSize=None)[0]
            except:
                daoPriceListProduct = ListinoArticolo()
                daoPriceListProduct.id_articolo = product_id
                daoPriceListProduct.id_listino = self.price_list_id
                daoPriceListProduct.data_listino_articolo = self.dataListino
                daoPriceListProduct.listino_attuale = True

            if self.prezzo_vendita_ivato is not None :
                prezzo = self.sanitizer(self.prezzo_vendita_ivato)
                #try:
                daoPriceListProduct.prezzo_dettaglio = mN(prezzo)
                #except:
                    #prezzo = self.checkDecimalSymbol(str(prezzo).strip(), decimalSymbol)
                    #daoPriceListProduct.prezzo_dettaglio = mN(prezzo)
            else:
                daoPriceListProduct.prezzo_dettaglio = 0

            if self.prezzo_vendita_non_ivato is not None:
                prezzo = self.sanitizer(self.prezzo_vendita_non_ivato)
                #try:
                daoPriceListProduct.prezzo_ingrosso = mN(prezzo)
                #except:
                    #prezzo = mN(self.checkDecimalSymbol(str(prezzo).split(), decimalSymbol))
                    #daoPriceListProduct.prezzo_ingrosso = prezzo
            else:
                daoPriceListProduct.prezzo_ingrosso = 0


            sconti_ingrosso = [ScontoVenditaIngrosso(),]
            sconti_dettaglio = [ScontoVenditaDettaglio(),]

            if self.sconto_vendita_ingrosso is not None and str(self.sconto_vendita_ingrosso).strip() != "0" and str(self.sconto_vendita_ingrosso).strip() !="":
                self.sconto_vendita_ingrosso = self.sanitizer(self.sconto_vendita_ingrosso)
                #try:
                sconti_ingrosso[0].valore = mN(self.sconto_vendita_ingrosso)
                sconti_ingrosso[0].tipo_sconto = 'percentuale'
                daoPriceListProduct.sconto_vendita_ingrosso = sconti_ingrosso
                #except:
                    #sconti_ingrosso[0].valore = mN(self.checkDecimalSymbol(self.sconto_vendita_ingrosso, decimalSymbol))
                    #sconti_ingrosso[0].tipo_sconto = 'percentuale'
                    #daoPriceListProduct.sconto_vendita_ingrosso = sconti_ingrosso

            if self.sconto_vendita_dettaglio is not None and str(self.sconto_vendita_dettaglio).strip() != "0" and str(self.sconto_vendita_dettaglio).strip() !="":
                self.sconto_vendita_dettaglio = self.sanitizer(self.sconto_vendita_dettaglio)
                #try:
                sconti_dettaglio[0].valore = mN(self.sconto_vendita_dettaglio)
                sconti_dettaglio[0].tipo_sconto = 'percentuale'
                daoPriceListProduct.sconto_vendita_dettaglio = sconti_dettaglio
                #except:
                    #sconti_dettaglio[0].valore = mN(self.checkDecimalSymbol(self.sconto_vendita_dettaglio, decimalSymbol))
                    #sconti_dettaglio[0].tipo_sconto = 'percentuale'
                    #daoPriceListProduct.sconto_vendita_dettaglio = sconti_dettaglio

            if self.prezzo_acquisto_non_ivato is not None and str(self.prezzo_acquisto_non_ivato).strip() != "0" and str(self.prezzo_acquisto_non_ivato).strip() !="":
                prezzo = self.sanitizer(self.prezzo_acquisto_non_ivato)

                #try:
                daoPriceListProduct.ultimo_costo = mN(prezzo)
                #except:
                    #prezzo = mN(self.checkDecimalSymbol(str(prezzo).strip(), decimalSymbol))
                    #daoPriceListProduct.ultimo_costo = prezzo
            elif self.prezzo_acquisto_ivato is not None and str(self.prezzo_acquisto_ivato).strip() != "0" and str(self.prezzo_acquisto_ivato).strip() !="":
                prezzo = self.sanitizer(self.prezzo_acquisto_ivato)
                self.aliquota_iva.percentuale = self.sanitizer(self.aliquota_iva.percentuale)
                #prezzo = prezzo.replace("€","")
                #prezzo = prezzo.replace(",",".")
                #try:
                daoPriceListProduct.ultimo_costo =  mN(calcolaPrezzoIva(mN(prezzo), -1 * (mN(self.aliquota_iva.percentuale))))
                #except:
                    #prezzo = mN(self.checkDecimalSymbol(str(prezzo).split(), decimalSymbol))
                    #daoPriceListProduct.ultimo_costo =  mN(calcolaPrezzoIva(mN(prezzo), -1 * mN(self.aliquota_iva.percentuale)))
            else:
                daoPriceListProduct.ultimo_costo = 0
            daoPriceListProduct.persist()

        # Fornitura
        daoFornitura = Fornitura().select(idFornitore=self.fornitore,
                                                    idArticolo=self.daoArticolo.id,
                                                    daDataPrezzo=self.dataListino,
                                                    aDataPrezzo=self.dataListino,
                                                    batchSize=None)
        if len(daoFornitura) == 0:
            daoFornitura = Fornitura()
            daoFornitura.prezzo_netto = prezzo or 0
            daoFornitura.prezzo_lordo = prezzo or 0
            daoFornitura.id_fornitore = self.fornitore
            daoFornitura.id_articolo = self.daoArticolo.id
            try:
                daoFornitura.percentuale_iva = Decimal(str(self.aliquota_iva.percentuale))
            except:
                daoFornitura.percentuale_iva = Decimal(str(self.aliquota_iva))
            daoFornitura.data_prezzo = self.dataListino
            daoFornitura.codice_articolo_fornitore = self.codice_fornitore
            daoFornitura.fornitore_preferenziale = True
            daoFornitura.persist()

    def checkDecimalSymbol(self, number, symbol):
        """ adjust non decimal simbols """
        if number is None:
            return str(0)

        if symbol == '.':
            number = str(number).replace(',','')
        elif symbol == ',':
            number = str(number).replace('.','')
            number = str(number).replace(',','.')
        return number

    def sanitizer(self,value):
        if value:
            value = value.strip()
            value = value.replace("€","")
            value = value.replace("%","")
            value = value.replace(",",".")
        return value
