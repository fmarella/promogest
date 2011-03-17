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

class Province(Dao):

    def __init__(self, req= None,arg=None):
        Dao.__init__(self, entity=self)

    def filter_values(self,k,v):
        dic= {
            'denominazione':province.c.denominazione == v,
                }
        return  dic[k]

std_mapper = mapper(Province, province, order_by=province.c.denominazione)

provi =[("001",'Torino',"TO"),
        ("002", 'Vercelli',"VC"),
        ("003",'Novara',"NO"),
        ("004",'Cuneo',"CN"),
        ("005", 'Asti',"AT"),
        ("006", 'Alessandria',"AL"),
        ("096",'Biella',"BI"),
        ("103",'Verbano-Cusio-Ossola',"VB"),
        ("007","Valle d'Aosta","AO"),
        ("012","Varese","VA"),
        ("013","Como","CO"),
        ("014","Sondrio","SO"),
        ("015","Milano","MI"),
        ("016","Bergamo","BG"),
        ("017","Brescia","BS"),
        ("018","Pavia","PV"),
        ("019","Cremona","CR"),
        ("020","Mantova","MN"),
        ("097","Lecco","LC"),
        ("098","Lodi","LO"),
        ("021","Bolzano","BZ"),
        ("022","Trento","TN"),
        ("023","Verona","VR"),
        ("024","Vicenza","VI"),
        ("025","Belluno","BL"),
        ("026","Treviso","TV"),
        ("027","Venezia","VE"),
        ("028","Padova","PD"),
        ("029","Rovigo","RO"),
        ("030","Udine","UD"),
        ("031","Gorizia","GO"),
        ("032","Trieste","TS"),
        ("093","Pordenone","PN"),
        ("008","Imperia","IM"),
        ("009","Savona","SV"),
        ("010","Genova","GE"),
        ("011","La Spezia","SP"),
        ("033","Piacenza","PC"),
        ("034","Parma","PR"),
        ("035","Reggio Emilia","RE"),
        ("036","Modena","MO"),
        ("037","Bologna","BO"),
        ("038","Ferrara","FE"),
        ("039","Ravenna","RA"),
        ("040","Forli'-Cesena","FC"),
        ("099","Rimini","RN"),
        ("045","Massa-Carrara","MS"),
        ("046","Lucca","LU"),
        ("047","Pistoia","PT"),
        ("048","Firenze","FI"),
        ("049","Livorno","LI"),
        ("050","Pisa","PI"),
        ("051","Arezzo","AR"),
        ("052","Siena","SI"),
        ("053","Grosseto","GR"),
        ("100","Prato","PO"),
        ("054","Perugia","PG"),
        ("055","Terni","TR"),
        ("041","Pesaro Urbino","PU"),
        ("042","Ancona","AN"),
        ("043","Macerata","MC"),
        ("044","Ascoli Piceno","AP"),
        ("056","Viterbo","VT"),
        ("057","Rieti","RI"),
        ("058","Roma","RM"),
        ("059","Latina","LT"),
        ("060","Frosinone","FR"),
        ("066","L'Aquila","AQ"),
        ("067","Teramo","TE"),
        ("068","Pescara","PE"),
        ("069","Chieti","CH"),
        ("070","Campobasso","CB"),
        ("094","Isernia","IS"),
        ("061","Caserta","CE"),
        ("062","Benevento","BN"),
        ("063","Napoli","NA"),
        ("064","Avellino","AV"),
        ("065","Salerno","SA"),
        ("071","Foggia","FG"),
        ("072","Bari","BA"),
        ("073","Taranto","TA"),
        ("074","Brindisi","BR"),
        ("075","Lecce","LE"),
        ("076","Potenza","PZ"),
        ("077","Matera","MT"),
        ("078","Cosenza","CS"),
        ("079","Catanzaro","CZ"),
        ("080","Reggio Calabria","RC"),
        ("101","Crotone","KR"),
        ("102","Vibo Valentia","VV"),
        ("081","Trapani","TP"),
        ("082","Palermo","PA"),
        ("083","Messina","ME"),
        ("084","Agrigento","AG"),
        ("085","Caltanissetta","CL"),
        ("086","Enna","EN"),
        ("087","Catania","CT"),
        ("088","Ragusa","RG"),
        ("089","Siracusa","SR"),
        ("090","Sassari","SS"),
        ("091","Nuoro","NU"),
        ("092","Cagliari","CA"),
        ("095","Oristano","OR"),
        ("104","Olbia-Tempio","OT"),
        ("105","Ogliastra","OG"),
        ("106","Medio Campidano","VS"),
        ("107","Carbonia-Iglesias","CI"),]

f = Province().select(denominazione="Nuoro")
if not f:
    for p in provi:
        a = Province()
        a.codice=p[0]
        a.denominazione = p[1]
        a.denominazione_breve=p[2]
        session.add(a)
    session.commit()
