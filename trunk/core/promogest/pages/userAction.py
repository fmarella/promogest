# -*- coding: utf-8 -*-

#    Copyright (C) 2005-2012 by Promotux
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

import hashlib
from sqlalchemy.orm import *
#from promogest.pages import *
from promogest.dao.User import User
from promogest.modules.RuoliAzioni.dao.Role import Role
from promogest.dao.PersonaGiuridica import PersonaGiuridica_ as PersonaGiuridica
from promogest.dao.Province import Province
from promogest.dao.Regioni import Regioni
#from core.dao.Cliente import Cliente
#from core.dao.Modulo import Modulo
#from core.dao.Canone import Canone
#from core.dao.Servizio import Servizio
#from core.dao.UserModule import UserModule
#from core.dao.UserService import UserService
#from core.dao.ClientProfile import ClientProfile
from promogest import Environment
from promogest.lib.webutils import *
from promogest.lib.page import Page
#from promogest.lib.MailHandler import *
from promogest.Environment import *

def user(req, subdomain=None, action=None):

    def userList(req,subdomain=None,action=None):
        """Funzione per la visualizzazione dei gli utenti
        """
        batch = 30
        order_by = req.args.get('order_by')
        changeOrder = req.args.get('asc')
        if not changeOrder:
             changeOrder = "1"
        if not order_by:
            order_by = desc(5)
        else:
            if changeOrder == "1":
                order_by = desc(int(order_by) or None)
            else:
                order_by = asc(int(order_by) or None)
        count = User(req=req).count(searchkey=req.form.get('searchkey'))
        args = pagination(req,batch,count)
        args["page_list"] = "siteAdmin/userList"
        users = User().select(searchkey=req.form.get('searchkey'),
                                batchSize=batch,
                                offset=args["offset"],
                                orderBy= order_by)
        roless = Role(req=req,).select(batchSize=None)
        pageData = {'file' : 'siteAdmin/userList',
                    "subdomain": addSlash(subdomain),
                    'roles' : roless,
                    'users' : users,
                    "args":args}
        return Page(req).render(pageData)

    def userAdd(req,subdomain=None,action=None):
        """
        Funzione per la aggiunta di nuovi utenti
        """
        update = False
        idrr = Session(req).getUserId()
        username = req.form.get('username')
        roles = Role(req=req).select(batchSize=None)
        if req.args.get('new') =="":
            # Add vuoto per cui non è un aggiornamento
            user = User(req=req)
            pageData = {'file' : 'userAdd',
                        "subdomain": addSlash(subdomain),
                        'roles':roles,
                        'user' : user}
            return Page(req).render(pageData)
        elif req.args.get("edit"):
#            id =req.args.get("edit")
#            return userDetail(id=id, subdomain=subdomain, req=req)
            user = User(req=req).getRecord(id =req.args.get("edit"))
            pageData = {'file' : 'userAdd',
                        "subdomain": addSlash(subdomain),
                        'roles':roles,
                        'user' : user}
            return Page(req).render(pageData)
        elif req.args.get('add') == ""\
                    and req.form.get('username')\
                    and req.form.get('password'):
            user = User(req=req)
        elif req.args.get('update') != ""\
                    and req.form.get('username') != "":
            user = User(req=req).getRecord(id =req.args.get("update"))
            update = True
        if user :
            password =req.form.get('password')
            re_password =req.form.get('re_password')
            email = req.form.get('email')
            photo_src = req.form.get('photo_src')
            id_role = req.form.get('roleId')
            if str(req.form.get('languageId')) :
                lng = str(req.form.get('languageId'))
            else:
                lng = "it"
            user.username = username
            user.id_language = lng
            user.email = email
            if update and password == "" and re_password == "":
                pass
            elif password == re_password:
                user.password = hashlib.md5(user.username + \
                                        password).hexdigest()

            user.id_role = id_role
            user.active = True
            user.persist()
            username = ''
            redirectUrl='/siteAdmin/userList'
            return Page(req).redirect(redirectUrl)
        else:
            pageData = {'file' : 'userAdd',
                        "subdomain": addSlash(subdomain),
                        'item': 1,
                        'roles' : roles}
            return Page(req).render(pageData)

    def userDel(req,subdomain=None,action=None):
        """
        Funzione per la cancellazione degli utenti
        """
        userId = req.args.get('id')
        if userId:
            user = User(req=req).getRecord(id=userId)
            if user.id_role not in [1]:
                user.delete()
                pg = PersonaGiuridica().select(id_user=userId)
                if pg:
                    cl = Cliente().getRecord(id=pg[0].id)
                    if cl:
                        cl.delete()
                    pg[0].delete()

            redirectUrl =addSlash(subdomain)+'siteAdmin/userList?pag='+str(req.args.get('pag'))
            return Page(req).redirect(redirectUrl)

        else:
            error = '<center>errore</center>'
            pageData = {'file' : 'error',
                        "subdomain": addSlash(subdomain),
                        'item': item,
                        'pag' : defaultOffsetIndex,
                        'error' : error}
            return Page(req).render(pageData)


    def userActive(req,subdomain=None, action=None):
        """
        Funzione che si occupa di gestire lo stato dell'user
        Attivo o disattivo
        """
        pgs= session.query(PersonaGiuridica).filter(PersonaGiuridica.id_user == None).all()
        if pgs:
            for p in pgs:
                cl = Cliente().getRecord(id=p.id)
                if cl:
                    cl.delete()
                p.delete()
        userId = req.args.get('id')
        if userId !='1':
            user = User(req=req).getRecord(id=userId)
            if user.active==False:
                user.active = True
            elif user.active==True:
                user.active = False
        user.persist()
        redirectUrl=addSlash(subdomain)+'/siteAdmin/userList'
        return Page(req).redirect(redirectUrl)



    def userMod(req,subdomain=None, action=None):
        """
        Funzione per la modifica dei dati utente
        """
        try:
            defaultOffsetIndex = int(req.args.get('pag'))-1
            if defaultOffsetIndex == 0:
                defaultOffset = 0
            else:
                defaultOffset = defaultOffsetIndex * Environment.params[self.path[1]]['defaultLimit']
        except:
                defaultOffsetIndex = 0
        userId = req.args.get('id')
        roles = Role(req=req).select(batchSize=None)
        try:
            pg = Dao(PersonaGiuridica, req=self.req).select(id_user=userId)
        except:
            pg= ''
        if userId:
            userDetail(req,onlyData=True)
            user = User(req=req).getRecord(id=userId)
            #print dir(user)
            #userRole = Role(req=req).getRecord(id=user.id_role)
            pageData = {'file' : 'userMod',
                        "subdomain": addSlash(subdomain),
                        'item': 1,
                        'pag' : defaultOffsetIndex,
                        'pg' : pg,
                        'roles' : roles,
                        #'dm' : self.dmm,
                        #'pg' : self.pgg,
                        #'telefono' : self.telefono,
                        #'fax' : self.faxx,
                        'user' : user}
            return Page(req).render(pageData)
        else:
            return Page(req).redirect('Error')


    def userUpdate(req, subdomain=None, action=None):
        """
        Funzione di gestione dei dati prelevati dal form di modifica
        """
        userId = str(req.form.get('id'))
        username = str(req.form.get('username'))
        password = str(req.form.get('password'))
        nome = str(req.form.get('nome'))
        cognome = str(req.form.get('cognome'))
        user = User(req=req).getRecord(id=userId)
        roleId = req.form.get('roleId')
        if password != '':
            user.password = hashlib.md5(user.username + password).hexdigest()
        user.id_role = roleId
        user.persist()
        redirectUrl = '/siteAdmin/userMod?id='+str(userId)
        return Page(req).redirect(redirectUrl)

    def userDetail(req=None,subdomain=None,action=None,onlyData=False, id=None):
        forms = req.form.to_dict()
        args = req.args.to_dict()
        print "FOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOORMS", forms
        if not id:
            idr = str(req.args.get('USER'))
        else:
            idr = id
        user = User(req=req).getRecord(id = idr)
        userId=user.id
        print "UUUUUUUUUUUUUUUUUUUUUUUUUUUSERRRRR", user
        pg = PersonaGiuridica().select(id_user=user.id)
        if not pg:
            print "Probabile cliente aggiunto da sito"
            cl = None
        else:
            cl = Cliente().getRecord(id=pg[0].id)
        province = Province().select(batchSize=None)
        regioni = Regioni().select(batchSize=None)
        if forms:
            user.pegi.nome = forms["nome"]
            user.pegi.cognome = forms["cognome"]
            user.pegi.ragione_sociale = forms["ragionesociale"]
            user.pegi.insegna = forms["insegna"]
            user.pegi.codice_fiscale = forms["codicefiscale"]
            user.pegi.partita_iva = forms["partitaiva"]
            user.pegi.id_sede_legale_provincia = int(forms["sedelegaleprovincia"])
            user.pegi.id_sede_legale_regione = int(forms["sedelegaleregione"])
            user.pegi.nazione = forms["sedelegalenazione"]
            if not cl:
                cl = Cliente()
            cl.id=pg[0].id
            cl.telefono = forms["telefono"]
            cl.fax = forms["fax"]
            cl.note = forms["note"]
            cl.persist()
            user.persist()
        print "ARRRRRRRRRRRRRRRRRRRRRRRRGS", args
        pageData = {'file' : 'userDetailSA',
#                "subdomain": subdomain,
                "forms":forms,
                "args":args,
                "user":user,
                "province": province,
                "regioni":regioni,
                "nazioni" :nationList,
                "cl":cl}
        return Page(req).render(pageData)

    def moduleHandler(moduliassociati, userId):
        m_old= UserModule().select(idUser = userId)
        m_ids = [ int(x) for x in moduliassociati]
        mold_ids = [ x.id_modulo for x in m_old]
        difference_dainserire=filter(lambda x:x not in mold_ids,m_ids)
        difference_dacancellare=filter(lambda x:x not in m_ids,mold_ids)
        for m in difference_dainserire:
            mod = UserModule()
            mod.id_user = userId
            mod.id_modulo = m
            if not mod.activation_date:
                mod.activation_date = datetime.datetime.now()
            mod.active= True
            mod.persist()
        for m in difference_dacancellare:
            mod = UserModule().select(idUser=userId,idModule=m)
            mod[0].delete()

    def serviceHandler(serviziassociati, userId):
        m_old= UserService().select(idUser = userId)
        m_ids = [ int(x) for x in serviziassociati]
        mold_ids = [ x.id_servizio for x in m_old]
        difference_dainserire=filter(lambda x:x not in mold_ids,m_ids)
        difference_dacancellare=filter(lambda x:x not in m_ids,mold_ids)
        for m in difference_dainserire:
            mod = UserService()
            mod.id_user = userId
            mod.id_servizio = m
            if not mod.activation_date:
                mod.activation_date = datetime.datetime.now()
            mod.active= True
            mod.persist()
        for m in difference_dacancellare:
            mod = UserService().select(idUser=userId,idService=m)
            mod[0].delete()

    def userPassword(req, subdomain=None, action=None):
        idr = str(req.args.get('id'))
        username = str(req.form.get('username'))
        password = str(req.form.get('password'))
        user = User(req=req).getRecord(id=idr)
        if password != '':
            user.password = hashlib.md5(user.username + password).hexdigest()
        user.id_role = roleId
        user.persist()
        redirectUrl = '/siteAdmin/userMod?id='+str(userId)
        return Page(req).redirect(redirectUrl)

    def userClienteEdit(req,subdomain=None,action=None):
        servizi = Servizio().select(batchSize=None)
        moduli = Modulo().select(batchSize=None)
        idr = str(req.args.get('id'))
        user = User(req=req).getRecord(id = idr)
        clienteprofile = ClientProfile().select(batchSize=None,idUser = user.id)
        forms = req.form.to_dict()
        canoni = Canone().select(idUser = user.id, batchSize=None)
        if not clienteprofile:
            clienteprofile = ClientProfile()
            clienteprofile.activation_date = datetime.datetime.now()
            clienteprofile.installation_code = createRandomString(num=15).upper()
            clienteprofile.id_user = user.id
            clienteprofile.active = True
            clienteprofile.persist()
            clienteprofile = ClientProfile().select(batchSize=None,idUser = user.id)

        if forms:
            print "FORMS",  forms
            if req.form.get('moduli'):
                moduliassociati = req.form.getlist('moduli')
                moduleHandler(moduliassociati, user.id)
            if req.form.get("servizi"):
                serviziassociati = req.form.getlist('servizi')
                serviceHandler(serviziassociati, user.id)
        userservice = [x.id_servizio for x in UserService().select(idUser = user.id)]
        usermodule = [x.id_modulo for x in UserModule().select(idUser = user.id)]
        pageData = {'file' : 'userCliente',
                "forms":forms,
                "moduli":moduli,
                "canoni": canoni,
                'userservice':userservice,
                'usermodule':usermodule,
                "servizi":servizi,
                'clienteprofile':clienteprofile[0],
                "user":user,
                }
        return Page(req).render(pageData)


    def userClienteSendInfo(req,subdomain=None,action=None):
        idr = str(req.args.get('id'))
        user = User(req=req).getRecord(id = idr)
        clienteprofile = ClientProfile().select(batchSize=None,idUser = user.id)
        usermodule = UserModule().select(idUser = user.id)
        canoni = Canone().select(idUser = user.id, batchSize=None)
        pageData = {"user" : user,
                    "clienteprofile": clienteprofile[0],
                    'usermodule':usermodule,
                    "usercanoni":canoni}
        html = renderizza(req,"user_client_send_info.html", pageData)
        SendMail(req=req,to=user.email).sendStdHTMLMail(html=html, subject="INFO PromoGest2")
        redirectUrl = '/siteAdmin/userList'
        return Page(req).redirect(redirectUrl)


    if action.upper() =="USERLIST":
        return userList(req,subdomain=subdomain, action=action)
    elif action.upper() == "USERMOD":
        return userMod(req,subdomain=subdomain,action=action)
    elif action.upper() == "USERDETAIL":
#        from core.pages.common.userDetail import userdetail
        return userDetail(req,subdomain=subdomain,action=action)
    elif action.upper() == "USERDEL":
        return userDel(req,subdomain=subdomain,action=action)
    elif action.upper() == "USERUPDATE":
        return userUpdate(req,subdomain=subdomain,action=action)
    elif action.upper() == "USERADD":
        return userAdd(req,subdomain=subdomain,action=action)
    elif action.upper() == "USERACTIVE":
        return userActive(req,subdomain=subdomain,action=action)
    elif action.upper() == "USERCLIENTEEDIT":
        return userClienteEdit(req,subdomain=subdomain,action=action)
    elif action.upper() == "USERPASSWORD":
        return userPassword(req,subdomain=subdomain,action=action)
    elif action.upper() == "USERCLIENTESENDINFO":
        return userClienteSendInfo(req,subdomain=subdomain,action=action)
