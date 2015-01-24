# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012,2011 by Promotux
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


    #def on_upgrade_iva_button_clicked(self, button):
        #from promogest.dao.Setconf import SetConf
        #kbb = SetConf().select(key="upgrade_iva_22", section="Articoli")
        #if kbb and kbb[0].value=="True":
            #messageInfo(msg="ATTENIONE, L'aggiornamento risuta già fatto\n si consiglia di richiudere la finestra di dialogo ")
        #fillComboboxAliquoteIva(self.iva_upgrade_combobox.combobox)
        #self.iva_upgrade_combobox.show_all()
        #self.crea_iva_radio.set_active(True)
        #self.upgrade_iva.show()
        ##self.upgrade_iva.destroy()

    #def on_esegui_upgrade_iva_button_clicked(self, button):
        #from promogest.dao.AliquotaIva import AliquotaIva
        #from promogest.dao.Articolo import Articolo
        #from promogest.dao.Setconf import SetConf
        #if self.scegli_iva_radio.get_active():
            #if not findIdFromCombobox(self.iva_upgrade_combobox.combobox):
                #messageError(msg= _("Selezionare l'aliquota al 22% dal menù a tendina!"))
                #return
            #else:
                #idAli = findIdFromCombobox(self.iva_upgrade_combobox.combobox)
                #ali = AliquotaIva().getRecord(id=idAli)
                #if ali.percentuale != 22:
                    #messageError(msg="ATTENZIONE, aliquota diversa da 22%")
                    #return

        #else:
            #ali = AliquotaIva().select(percentuale=22,idTipo=1)
            #if ali:
                #messageError(msg="Aliquota iva al 22% già presente, uso quella")
                #idAli = ali[0].id
            #else:
                #a = AliquotaIva()
                #a.denominazione = "Aliquota IVA 22%"
                #a.denominazione_breve = "22%"
                #a.id_tipo = 1
                #a.percentuale = 22
                #a.persist()
                #idAli = a.id

        #vecchiaIva = AliquotaIva().select(percentuale=21,idTipo=1)
        #vecchiaIdIva = None
        #if not vecchiaIva:
            #messageError(msg="NON RIESCO A TROVARE UNA ALIQUOTA IVA AL 21 NEL SISTEMA")
            #return
        #else:
            #if len(vecchiaIva) >1:
                #messageInfo(msg= "PIÙ DI UNA IVA AL 21% PRESENTE \n contattare l'assistenza")
                #return
            #else:
                #vecchiaIdIva = vecchiaIva[0].id
        #arti = Articolo().select(idAliquotaIva=vecchiaIdIva, batchSize=None)
        #if not arti:
            #messageInfo(msg="Nessun articolo con iva al 21% trovato")
            #kbb = SetConf().select(key="upgrade_iva_22", section="Articoli")
            #if not kbb:
                #kbb = SetConf()
                #kbb.key = "upgrade_iva_22"
                #kbb.value ="True"
                #kbb.section = "Articoli"
                #kbb.tipo_section = "Generico"
                #kbb.description = "upgrade_iva_22%"
                #kbb.active = True
                #kbb.tipo = "bool"
                #kbb.date = datetime.now()
                #kbb.persist()
            #else:
                #kbb[0].value="True"
                #kbb[0].persist()
        #else:
            #for a in arti:
                #a.id_aliquota_iva = idAli
                #Environment.session.add(a)
            #Environment.session.commit()
            #messageInfo(msg="PROCESSO TERMINATO!")
            #kbb = SetConf().select(key="upgrade_iva_22", section="Articoli")
            #if not kbb:
                #kbb = SetConf()
                #kbb.key = "upgrade_iva_22"
                #kbb.value ="True"
                #kbb.section = "Articoli"
                #kbb.tipo_section = "Generico"
                #kbb.description = "upgrade_iva_22%"
                #kbb.active = True
                #kbb.tipo = "bool"
                #kbb.date = datetime.now()
                #kbb.persist()
            #else:
                #kbb[0].value="True"
                #kbb[0].persist()

    #def on_scegli_iva_radio_toggled(self, radioButton):
        #if radioButton.get_active():
            #print "CREA"
            #self.iva_upgrade_combobox.set_sensitive(True)
        #else:
            #print "SELEZIONA"
            #self.iva_upgrade_combobox.set_sensitive(False)

    #def on_upgrade_iva_chiudi_button_clicked(self, button):
        ##print " MA INSMMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        #self.upgrade_iva.hide()
        ##self.show()


#from sqlalchemy import MetaData
#from sqlalchemy_schemadisplay import create_schema_graph

## create the pydot graph object by autoloading all tables via a bound metadata object
#graph = create_schema_graph(metadata=Environment.meta,
   #show_datatypes=True, # The image would get nasty big if we'd show the datatypes
   #show_indexes=True, # ditto for indexes
   #rankdir='LR', # From left to right (instead of top to bottom)
   #concentrate=True # Don't try to join the relation lines together
#)
#graph.write_png('dbschema.png') # write out the file


#from promogest.dao.Articolo import Articolo
#from sqlalchemy_schemadisplay import create_uml_graph
#from sqlalchemy.orm import class_mapper

## lets find all the mappers in our model
#mappers = []
#for attr in dir(Articolo):
    #print "AAAAAAAAAAAATRRR", attr
    #if attr[0] == '_': continue
    #try:
        #cls = getattr(Articolo, attr)
        #mappers.append(class_mapper(cls))
    #except:
        #pass

## pass them to the function and set some formatting options
#graph = create_uml_graph(mappers,
    #show_operations=False, # not necessary in this case
    #show_multiplicity_one=False # some people like to see the ones, some don't
#)
#graph.write_png('schema.png') # write out the file
