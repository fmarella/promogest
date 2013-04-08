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


        #if datetime.date.today() >= datetime.date(2011,9,17):
            #from promogest.dao.Setconf import SetConf
            #kbb = SetConf().select(key="upgrade_iva", section="Articoli")
            #if kbb and kbb[0].value=="True":
                #return
            #else:
                #fillComboboxAliquoteIva(self.iva_upgrade_combobox.combobox)
                #self.iva_upgrade_combobox.show_all()
                #self.crea_iva_radio.set_active(True)
                #self.upgrade_iva.run()


    # def on_apri_dialog_upgrade_iva_button_clicked(self, button):
        # from promogest.dao.Setconf import SetConf
        # kbb = SetConf().select(key="upgrade_iva", section="Articoli")
        # if kbb and kbb[0].value=="True":
            # messageInfo(msg="ATTENIONE, L'aggiornamento risuta già fatto\n si consiglia di richiudere la finestra di dialogo ")
        # fillComboboxAliquoteIva(self.iva_upgrade_combobox.combobox)
        # self.iva_upgrade_combobox.show_all()
        # self.crea_iva_radio.set_active(True)
        # self.upgrade_iva.run()

    # def on_esegui_upgrade_iva_button_clicked(self, button):
        # from promogest.dao.AliquotaIva import AliquotaIva
        # from promogest.dao.Articolo import Articolo
        # from promogest.dao.Setconf import SetConf
        # if self.scegli_iva_radio.get_active():
            # if not findIdFromCombobox(self.iva_upgrade_combobox.combobox):
                # messageError(msg= _("Selezionare l'aliquota al 21% dal menù a tendina!"))
                # return
            # else:
                # idAli = findIdFromCombobox(self.iva_upgrade_combobox.combobox)
                # ali = AliquotaIva().getRecord(id=idAli)
                # if ali.percentuale != 21:
                    # messageError(msg="ATTENZIONE, aliquota diversa da 21%")
                    # return

        # else:
            # ali = AliquotaIva().select(percentuale=21,idTipo=1)
            # if ali:
                # messageError(msg="Aliquota iva al 21% già presente, uso quella")
                # idAli = ali[0].id
            # else:
                # a = AliquotaIva()
                # a.denominazione = "Aliquota IVA 21%"
                # a.denominazione_breve = "21%"
                # a.id_tipo = 1
                # a.percentuale = 21
                # a.persist()
                # idAli = a.id

        # vecchiaIva = AliquotaIva().select(percentuale=20,idTipo=1)
        # vecchiaIdIva = None
        # if not vecchiaIva:
            # messageError(msg="NON RIESCO A TROVARE UNA ALIQUOTA IVA AL 20 NEL SISTEMA")
            # return
        # else:
            # if len(vecchiaIva) >1:
                # messageInfo(msg= "PIÙ DI UNA IVA AL 20% PRESENTE \n contattare l'assistenza")
                # return
            # else:
                # vecchiaIdIva = vecchiaIva[0].id
        #print "sono pronto a ciclare sugli articoli", idAli, vecchiaIdIva
        # arti = Articolo().select(idAliquotaIva=vecchiaIdIva, batchSize=None)
        # if not arti:
            # messageInfo(msg="Nessun articolo con iva al 20% trovato")
            # kbb = SetConf().select(key="upgrade_iva", section="Articoli")
            # if not kbb:
                # kbb = SetConf()
                # kbb.key = "upgrade_iva"
                # kbb.value ="True"
                # kbb.section = "Articoli"
                # kbb.tipo_section = "Generico"
                # kbb.description = "upgrade_iva_21%"
                # kbb.active = True
                # kbb.tipo = "bool"
                # kbb.date = datetime.datetime.now()
                # kbb.persist()
            # else:
                # kbb[0].value="True"
                # kbb[0].persist()
        # else:
            # for a in arti:
                # a.id_aliquota_iva = idAli
                # Environment.session.add(a)
            # Environment.session.commit()
            # messageInfo(msg="PROCESSO TERMINATO!!!!!")
            # kbb = SetConf().select(key="upgrade_iva", section="Articoli")
            # if not kbb:
                # kbb = SetConf()
                # kbb.key = "upgrade_iva"
                # kbb.value ="True"
                # kbb.section = "Articoli"
                # kbb.tipo_section = "Generico"
                # kbb.description = "upgrade_iva_21%"
                # kbb.active = True
                # kbb.tipo = "bool"
                # kbb.date = datetime.datetime.now()
                # kbb.persist()
            # else:
                # kbb[0].value="True"
                # kbb[0].persist()


    # def on_scegli_iva_radio_toggled(self, radioButton):
        # if radioButton.get_active():
            #print "CREA"
            # self.iva_upgrade_combobox.set_sensitive(True)
        # else:
            #print "SELEZIONA"
            # self.iva_upgrade_combobox.set_sensitive(False)

    # def on_upgrade_iva_chiudi_button_clicked(self, button):
        # self.upgrade_iva.hide()