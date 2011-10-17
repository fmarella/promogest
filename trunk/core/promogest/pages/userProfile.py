#-*- coding: utf-8 -*-
#
# Promogest -Janas
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>
# Author: Andrea Maccis <amaccis@promotux.it>


import md5
from core import Environment
from core.utils import *
from pages import *
from core.dao.User import User
from core.dao.Cliente import Cliente
from core.dao.Contatto import Contatto
from core.dao.ContattoCliente import ContattoCliente
from core.dao.RecapitoContatto import RecapitoContatto
from core.dao.PersonaGiuridica import PersonaGiuridica_
from core.dao.DestinazioneMerce import DestinazioneMerce
from core.dao.ClienteCategoriaCliente import ClienteCategoriaCliente
from core.session import Session
from core.page import Page
import datetime


class UserProfile(object):

    def __init__(self, req):
        """ classe complessa ed incasinata per l'inserimento dei dati utente
            wayd = what are you doing
        """
        self.req = req
        self.path = req.environ['PATH_INFO'].split('/')

    def userProfile(self):
        """ Funzione di visualizzazione dai completi utente
        """
        if str(self.req.args.get('id'))!="None":
            self.userId = str(self.req.args.get('id'))
        else:
            self.userId = Session(self.req).getUserId()

        self.user = Dao(User,req=self.req).getRecord(id=self.userId)

        self.pg = PersonaGiuridica(req=self.req)
        self.dm = DestinazioneMerce(req=self.req)
        self.contact = Contatto(req=self.req)
        self.recapito = Recapito(req=self.req)
        self.clCatCl = ClienteCategoriaCliente(req=self.req)
        self.telefono = ""
        self.fax = ""
        self.url = ""
        self.act = findAct(self.req)
        self.formData = {}
        for keys, values in self.req.form.iterlists():
            exec "self.formData[keys] = values[0]"
        print "LA CHIAVE E QUI ", self.formData
        if str(self.req.form.get('wayd')) == "ins":
            # inserimento dati utente
            self.insertProfile()
            if self.act:
                if self.act == 'reg':
                    self.user.active = False
                    dati = {
                        'nome' : self.formData['nome'],
                        'cognome' : self.formData['cognome'],
                        'ragione_sociale' : self.formData['ragione_sociale'],
                        'codice_fiscale' : self.formData['codice_fiscale'],
                        'partita_iva' : self.formData['partita_iva'],
                        'indirizzo' : self.formData['sede_legale_indirizzo'],
                        'localita' : self.formData['sede_legale_localita'],
                        'provincia' : self.formData['sede_legale_provincia'],
                        'cap' : self.formData['sede_legale_cap'],
                        'email' : self.formData['email']
                    }
                    email = str(Environment.params[self.path[1]]['fromaddr'])
                    #SendMail(req=req,email=self.recapitoEmail).sendRegMail(dati=dati)
                    SendMail(req=self.req,email=email).sendRegMail(dati=dati)
                    Session(self.req).destroy()
                    redirectUrl = 'registerForm'
                    return Page(self.req).redirect(redirectUrl)
                    resp = RedirectResponse(redirectUrl)
                else:
                    redirectUrl = 'userProfile'
                    cookiename = self.path[1]+'buy'
                    cookieval = 'step3'
                    return Page(self.req).redirect(redirectUrl, cookiename, cookieval)
            return Page(self.req).redirect()
        if str(self.req.form.get('wayd')) == "up":
            self.insertProfile()
            if self.act:
                redirectUrl = 'buy'
                cookiename = self.path[1]+'buy'
                cookieval = 'step3'
                return Page(self.req).redirect(redirectUrl, cookiename, cookieval)
            else:
                if getRoleFromId(self.req)=="Admin":
                    redirectUrl = 'siteAdmin/user/userList'
                else:
                    redirectUrl = 'userProfile'
                return Page(self.req).redirect(redirectUrl)
        if PersonaGiuridica(req=self.req).select(id_user = self.userId):
            wayd = "up"
        else:
            wayd = "ins"
        #if not req.form.get('update'):
        #role = getRoleFromId(self.req)
        #print "ROLEEEEEEEEEEEEEEEEEEEEESS", role
        try:
            self.pg = PersonaGiuridica(req = self.req).select(id_user = self.userId)[0]
        except:
            print _("Dati della persona giuridica NON presenti al momento")
            #pass
        try:
            self.dm = DestinazioneMerce(req=self.req).select(id_cliente = self.pg.id)
        except:
            print _("Dati della destinazione merce NON presenti al momento")
            #pass
        try:
            contactClienteId = ContattoCliente(req=self.req).select(id_cliente = self.pg.id)[0]
            tel = Recapito(req=self.req).select(id_contatto = contactClienteId.id,tipo_recapito = "Telefono")[0]
            self.telefono = tel.recapito
        except:
            print _("Nessun recapito telefonico presente al momento")
            #pass
        try:
            contactClienteId = ContattoCliente(req=self.req).select(id_cliente = self.pg.id)[0]
            self.contact = Contatto(req=self.req).getRecord(id=(contactClienteId.id, contactClienteId.tipo_contatto))
        except:
            print _("Nessun Contatto presente al momento")
            #pass
        try:
            contactClienteId = ContattoCliente(req=self.req).select(id_cliente = self.pg.id)[0]
            fax = Recapito(req=self.req).select(id_contatto = contactClienteId.id,tipo_recapito = "Fax")[0]
            self.fax = fax.recapito
        except:
            print _("Nessun Fax presente al momento")
            #pass
        try:
            contactClienteId = ContattoCliente(req=self.req).select(id_cliente = self.pg.id)[0]
            url = Recapito(req=self.req).select(id_contatto = contactClienteId.id,tipo_recapito = "Url")[0]
            self.url = url.recapito
        except:
            print _("Nessun URL presente al momento")
        pageData = {'file' : 'userProfile',
                    'pg' : self.pg,
                    'dm' : self.dm,
                    'wayd' : wayd,
                    'act' : self.act,
                    'telefono' : self.telefono,
                    'fax' : self.fax,
                    'url':self.url,
                    'contact' : self.contact,
                    'recapito' : self.recapito,
                    'user' : self.user
                        }
        return Page(self.req).render(pageData)

    def insertProfile(self):
        print _("###### INSERT o UPDATE######")
        #if self.req.form.get('user'):
            #self.user = self.req.form.get('user')
        #if self.req.form.get('password'):
            #self.passwd = self.req.form.get('password')
        user = User(req=self.req).getRecord(id=self.userId)
        passwd = self.formData['passwd'] #self.passwd
        passcnf = self.formData['passwd'] #self.passcnf
        if passwd !="" and passwd !="" and passwd==passcnf:
            user.password = md5.new(user.username + str(passwd)).hexdigest()
        if str(self.req.form.get('languageId')) :
            lng = str(self.req.form.get('languageId'))
        else:
            lng = "it"
        user.id_language = lng
        user.email = self.formData['email']
        user.last_modified= str(datetime.datetime.utcnow())
        user.persist()
        try:
            pgl = PersonaGiuridica(req=self.req).select(id_user=self.userId)
            if len(pgl)>1:
                error = """<br/><br/><center>ATTENZIONE. Errore di integrita'
                nel Database. Contattare  il Webmaster francesco@promotux.it, 800034561</center>"""
                pageData = {'file' : 'error',
                        'error' : error}
                return Page(self.req).render(pageData)
            else:
                pg = pgl[0]
        except:
            pg = PersonaGiuridica(req=self.req)
        pg.codice = "web"
        pg.ragione_sociale = self.formData['ragione_sociale']
        pg.insegna = self.formData['insegna']
        pg.nome = self.formData['nome']
        pg.cognome = self.formData['cognome']
        pg.sede_operativa_indirizzo = self.formData['sede_operativa_indirizzo']
        pg.sede_operativa_cap = self.formData['sede_operativa_cap']
        pg.sede_operativa_localita = self.formData['sede_operativa_localita']
        pg.sede_operativa_provincia = self.formData['sede_operativa_provincia']
        pg.sede_legale_indirizzo = self.formData['sede_legale_indirizzo']
        pg.sede_legale_cap = self.formData['sede_legale_cap']
        pg.sede_legale_localita = self.formData['sede_legale_localita']
        pg.sede_legale_provincia = self.formData['sede_legale_provincia']
        pg.nazione = self.formData['nazione']
        pg.codice_fiscale = self.formData['codice_fiscale']
        pg.partita_iva= self.formData['partita_iva']
        pg.id_user = self.userId
        pg.persist()
        #Da considerare che si potranno agganciare dati relativi alla banca o al tipo pagamento
        if not Cliente(req=self.req).getRecord(id=pg.id):
            cliente = Cliente(req=self.req)
            cliente.id = pg.id
        else:
            cliente = Cliente(req=self.req).getRecord(id=pg.id)
        cliente.persist()
        if ContattoCliente(req=self.req).select(id_cliente=cliente.id) ==[]:
            contactCliente = ContattoCliente(req=self.req)
            contactCliente.id_cliente = cliente.id
            contactCliente.tipo_contatto = "cliente"
        else:
            contactCliente = ContattoCliente(req=self.req).select(id_cliente=cliente.id)[0]
        contactCliente.persist()
        if not Contatto(req=self.req).getRecord(id=(contactCliente.id,contactCliente.tipo_contatto)):
            contact = Contatto(req=self.req)
            contact.note = self.formData['note']
            contact.descrizione = "Web"
            contact.tipo_contatto = "cliente"
        else:
            contact = Contatto(req=self.req).getRecord( id=(contactCliente.id,contactCliente.tipo_contatto))
            contact.note = self.formData['note']
            contact.descrizione = "Web"
            contact.tipo_contatto = "cliente"
        #contact.contatto_id
        contact.persist()
        #try:

        #self.clCatCl = Dao(ClienteCategoriaCliente, req=self.req).getRecord()
        #self.clCatCl.id_cliente = self.cliente.id
        #self.clCatCl.id_categoria_cliente = "1"
        #self.clCatCl.persist()
        try:
            if self.formData['destinazione_indirizzo'] or self.formData['destinazione_denominazione']:
                dm = DestinazioneMerce(req=self.req)
                dm.denominazione = self.formData['destinazione_denominazione']
                dm.localita = self.formData['destinazione_localita']
                dm.indirizzo = self.formData['destinazione_indirizzo']
                dm.cap = self.formData['destinazione_cap']
                dm.provincia = self.formData['destinazione_provincia']
                dm.id_cliente = self.cliente.id
                dm.persist()
        except:
            print _("attenzione destinazione non definita")
            #dm.flush(self.req)

        if self.formData['email']:
            try:
                contactClienteId = ContattoCliente(req=self.req).select(id_cliente = pg.id)[0]
                recapitoEmail = Recapito(req=self.req).select(id_contatto = contactClienteId.id,tipo_recapito = "E-Mail")[0]
            except:
                recapitoEmail = Recapito(req=self.req)
            recapitoEmail.tipo_recapito = "E-Mail"
            recapitoEmail.recapito = self.formData['email']
            recapitoEmail.id_contatto = contact.id
            recapitoEmail.persist()

        if self.formData['telefono']:
            try:
                contactClienteId = ContattoCliente(req=self.req)).select(id_cliente = pg.id)[0]
                recapitoTel = Recapito(req=self.req)).select(id_contatto = contactClienteId.id,tipo_recapito = "Telefono")[0]
            except:
                recapitoTel = Recapito(req=self.req)
            recapitoTel.tipo_recapito = "Telefono"
            recapitoTel.recapito= self.formData['telefono']
            recapitoTel.id_contatto = contact.id
            recapitoTel.persist()

        if self.formData['fax']:
            try:
                contactClienteId = ContattoCliente(req=self.req).select(id_cliente = pg.id)[0]
                recapitoFax = Recapito(req=self.req).select(id_contatto = contactClienteId.id,tipo_recapito = "Fax")[0]
            except:
                recapitoFax = Dao(Recapito, req=self.req).getRecord()
            recapitoFax.tipo_recapito = "Fax"
            recapitoFax.recapito = self.formData['fax']
            recapitoFax.id_contatto = contact.id
            recapitoFax.persist()

        if self.formData['url']:
            try:
                contactClienteId = ContattoCliente(req=self.req).select(id_cliente = pg.id)[0]
                recapitoUrl = Recapito(req=self.req).select(id_contatto = contactClienteId.id,tipo_recapito = "Url")[0]
            except:
                recapitoUrl = Recapito(req=self.req)
            recapitoUrl.tipo_recapito = "Url"
            recapitoUrl.recapito= self.formData['url']
            recapitoUrl.id_contatto = contact.id
            recapitoUrl.persist()


