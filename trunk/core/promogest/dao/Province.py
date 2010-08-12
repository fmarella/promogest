#-*- coding: utf-8 -*-
#
# Promogest -Janas
#
# Copyright (C) 2009 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from sqlalchemy import *
from sqlalchemy.orm import *
from promogest.Environment import *
from Dao import Dao


try:
    province=Table('provincia', params['metadata'],schema = params['mainSchema'],autoload=True)
except:
    province  = Table('provincia', params["metadata"],
            Column('id',Integer,primary_key=True),
            Column('denominazione',String(100)),
            Column('denominazione_breve',String(2)),
            Column('codice',Integer),
            schema = params['mainSchema'])

    province.create(checkfirst=True)
    s= select([province.c.denominazione]).execute().fetchall()
    if (u'Torino',) not in s or s ==[]:
        tipo = province.insert()
        tipo.execute(codice = "001", denominazione='Torino',denominazione_breve="TO")
        tipo.execute(codice = "002", denominazione='Vercelli',denominazione_breve="VC")
        tipo.execute(codice = "003", denominazione='Novara',denominazione_breve="NO")
        tipo.execute(codice = "004", denominazione='Cuneo',denominazione_breve="CN")
        tipo.execute(codice = "005", denominazione='Asti',denominazione_breve="AT")
        tipo.execute(codice = "006", denominazione='Alessandria',denominazione_breve="AL")
        tipo.execute(codice = "096", denominazione='Biella',denominazione_breve="BI")
        tipo.execute(codice = "103", denominazione='Verbano-Cusio-Ossola',denominazione_breve="VB")
        tipo.execute(codice = "007", denominazione="Valle d'Aosta",denominazione_breve="AO")
        tipo.execute(codice = "012", denominazione="Varese",denominazione_breve="VA")
        tipo.execute(codice = "013", denominazione="Como",denominazione_breve="CO")
        tipo.execute(codice = "014", denominazione="Sondrio",denominazione_breve="SO")
        tipo.execute(codice = "015", denominazione="Milano",denominazione_breve="MI")
        tipo.execute(codice = "016", denominazione="Bergamo",denominazione_breve="BG")
        tipo.execute(codice = "017", denominazione="Brescia",denominazione_breve="BS")
        tipo.execute(codice = "018", denominazione="Pavia",denominazione_breve="PV")
        tipo.execute(codice = "019", denominazione="Cremona",denominazione_breve="CR")
        tipo.execute(codice = "020", denominazione="Mantova",denominazione_breve="MN")
        tipo.execute(codice = "097", denominazione="Lecco",denominazione_breve="LC")
        tipo.execute(codice = "098", denominazione="Lodi",denominazione_breve="LO")
        tipo.execute(codice = "021", denominazione="Bolzano",denominazione_breve="BZ")
        tipo.execute(codice = "022", denominazione="Trento",denominazione_breve="TN")
        tipo.execute(codice = "023", denominazione="Verona",denominazione_breve="VR")
        tipo.execute(codice = "024", denominazione="Vicenza",denominazione_breve="VI")
        tipo.execute(codice = "025", denominazione="Belluno",denominazione_breve="BL")
        tipo.execute(codice = "026", denominazione="Treviso",denominazione_breve="TV")
        tipo.execute(codice = "027", denominazione="Venezia",denominazione_breve="VE")
        tipo.execute(codice = "028", denominazione="Padova",denominazione_breve="PD")
        tipo.execute(codice = "029", denominazione="Rovigo",denominazione_breve="RO")
        tipo.execute(codice = "030", denominazione="Udine",denominazione_breve="UD")
        tipo.execute(codice = "031", denominazione="Gorizia",denominazione_breve="GO")
        tipo.execute(codice = "032", denominazione="Trieste",denominazione_breve="TS")
        tipo.execute(codice = "093", denominazione="Pordenone",denominazione_breve="PN")
        tipo.execute(codice = "008", denominazione="Imperia",denominazione_breve="IM")
        tipo.execute(codice = "009", denominazione="Savona",denominazione_breve="SV")
        tipo.execute(codice = "010", denominazione="Genova",denominazione_breve="GE")
        tipo.execute(codice = "011", denominazione="La Spezia",denominazione_breve="SP")
        tipo.execute(codice = "033", denominazione="Piacenza",denominazione_breve="PC")
        tipo.execute(codice = "034", denominazione="Parma",denominazione_breve="PR")
        tipo.execute(codice = "035", denominazione="Reggio Emilia",denominazione_breve="RE")
        tipo.execute(codice = "036", denominazione="Modena",denominazione_breve="MO")
        tipo.execute(codice = "037", denominazione="Bologna",denominazione_breve="BO")
        tipo.execute(codice = "038", denominazione="Ferrara",denominazione_breve="FE")
        tipo.execute(codice = "039", denominazione="Ravenna",denominazione_breve="RA")
        tipo.execute(codice = "040", denominazione="Forli'-Cesena",denominazione_breve="FC")
        tipo.execute(codice = "099", denominazione="Rimini",denominazione_breve="RN")
        tipo.execute(codice = "045", denominazione="Massa-Carrara",denominazione_breve="MS")
        tipo.execute(codice = "046", denominazione="Lucca",denominazione_breve="LU")
        tipo.execute(codice = "047", denominazione="Pistoia",denominazione_breve="PT")
        tipo.execute(codice = "048", denominazione="Firenze",denominazione_breve="FI")
        tipo.execute(codice = "049", denominazione="Livorno",denominazione_breve="LI")
        tipo.execute(codice = "050", denominazione="Pisa",denominazione_breve="PI")
        tipo.execute(codice = "051", denominazione="Arezzo",denominazione_breve="AR")
        tipo.execute(codice = "052", denominazione="Siena",denominazione_breve="SI")
        tipo.execute(codice = "053", denominazione="Grosseto",denominazione_breve="GR")
        tipo.execute(codice = "100", denominazione="Prato",denominazione_breve="PO")
        tipo.execute(codice = "054", denominazione="Perugia",denominazione_breve="PG")
        tipo.execute(codice = "055", denominazione="Terni",denominazione_breve="TR")
        tipo.execute(codice = "041", denominazione="Pesaro Urbino",denominazione_breve="PU")
        tipo.execute(codice = "042", denominazione="Ancona",denominazione_breve="AN")
        tipo.execute(codice = "043", denominazione="Macerata",denominazione_breve="MC")
        tipo.execute(codice = "044", denominazione="Ascoli Piceno",denominazione_breve="AP")
        tipo.execute(codice = "056", denominazione="Viterbo",denominazione_breve="VT")
        tipo.execute(codice = "057", denominazione="Rieti",denominazione_breve="RI")
        tipo.execute(codice = "058", denominazione="Roma",denominazione_breve="RM")
        tipo.execute(codice = "059", denominazione="Latina",denominazione_breve="LT")
        tipo.execute(codice = "060", denominazione="Frosinone",denominazione_breve="FR")
        tipo.execute(codice = "066", denominazione="L'Aquila",denominazione_breve="AQ")
        tipo.execute(codice = "067", denominazione="Teramo",denominazione_breve="TE")
        tipo.execute(codice = "068", denominazione="Pescara",denominazione_breve="PE")
        tipo.execute(codice = "069", denominazione="Chieti",denominazione_breve="CH")
        tipo.execute(codice = "070", denominazione="Campobasso",denominazione_breve="CB")
        tipo.execute(codice = "094", denominazione="Isernia",denominazione_breve="IS")
        tipo.execute(codice = "061", denominazione="Caserta",denominazione_breve="CE")
        tipo.execute(codice = "062", denominazione="Benevento",denominazione_breve="BN")
        tipo.execute(codice = "063", denominazione="Napoli",denominazione_breve="NA")
        tipo.execute(codice = "064", denominazione="Avellino",denominazione_breve="AV")
        tipo.execute(codice = "065", denominazione="Salerno",denominazione_breve="SA")
        tipo.execute(codice = "071", denominazione="Foggia",denominazione_breve="FG")
        tipo.execute(codice = "072", denominazione="Bari",denominazione_breve="BA")
        tipo.execute(codice = "073", denominazione="Taranto",denominazione_breve="TA")
        tipo.execute(codice = "074", denominazione="Brindisi",denominazione_breve="BR")
        tipo.execute(codice = "075", denominazione="Lecce",denominazione_breve="LE")
        tipo.execute(codice = "076", denominazione="Potenza",denominazione_breve="PZ")
        tipo.execute(codice = "077", denominazione="Matera",denominazione_breve="MT")
        tipo.execute(codice = "078", denominazione="Cosenza",denominazione_breve="CS")
        tipo.execute(codice = "079", denominazione="Catanzaro",denominazione_breve="CZ")
        tipo.execute(codice = "080", denominazione="Reggio Calabria",denominazione_breve="RC")
        tipo.execute(codice = "101", denominazione="Crotone",denominazione_breve="KR")
        tipo.execute(codice = "102", denominazione="Vibo Valentia",denominazione_breve="VV")
        tipo.execute(codice = "081", denominazione="Trapani",denominazione_breve="TP")
        tipo.execute(codice = "082", denominazione="Palermo",denominazione_breve="PA")
        tipo.execute(codice = "083", denominazione="Messina",denominazione_breve="ME")
        tipo.execute(codice = "084", denominazione="Agrigento",denominazione_breve="AG")
        tipo.execute(codice = "085", denominazione="Caltanissetta",denominazione_breve="CL")
        tipo.execute(codice = "086", denominazione="Enna",denominazione_breve="EN")
        tipo.execute(codice = "087", denominazione="Catania",denominazione_breve="CT")
        tipo.execute(codice = "088", denominazione="Ragusa",denominazione_breve="RG")
        tipo.execute(codice = "089", denominazione="Siracusa",denominazione_breve="SR")
        tipo.execute(codice = "090", denominazione="Sassari",denominazione_breve="SS")
        tipo.execute(codice = "091", denominazione="Nuoro",denominazione_breve="NU")
        tipo.execute(codice = "092", denominazione="Cagliari",denominazione_breve="CA")
        tipo.execute(codice = "095", denominazione="Oristano",denominazione_breve="OR")
        tipo.execute(codice = "104", denominazione="Olbia-Tempio",denominazione_breve="OT")
        tipo.execute(codice = "105", denominazione="Ogliastra",denominazione_breve="OG")
        tipo.execute(codice = "106", denominazione="Medio Campidano",denominazione_breve="VS")
        tipo.execute(codice = "107", denominazione="Carbonia-Iglesias",denominazione_breve="CI")


class Province(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {
            'denominazione':province.c.denominazione == v,
                }
        return  dic[k]

std_mapper = mapper(Province, province, order_by=province.c.denominazione)
