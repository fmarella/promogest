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

import Image
import math
import os
import random
import re
import feedparser
from werkzeug.wrappers import BaseRequest, BaseResponse
from werkzeug import FileStorage
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
from promogest import Environment
from Sla2Pdf_ng import Sla2Pdf_ng
#from core.DateFormat import DateFormat
from session import Session
from promogest.lib.postmarkup import *
from promogest.modules.RuoliAzioni.dao.Role import Role
from promogest.modules.RuoliAzioni.dao.RoleAction import RoleAction
from promogest.modules.RuoliAzioni.dao.Action import Action
from promogest.dao.User import User
#from core.dao.Feed import Feed
#from core.dao.Subdomain import Subdomain
from promogest.dao.Setconf import SetConf
from  promogest.ui import utils
import Image, ImageDraw
from random import randint as rint
import ImageFont

#from promoCMS.page import Page
from jinja2 import Environment  as Env
from jinja2 import FileSystemLoader,FileSystemBytecodeCache,environmentfilter, Markup, escape
url_map = Map()

def expose(rule, **kw):
    def decorate(f):
        kw['endpoint'] = f.__name__
        url_map.add(Rule(rule, **kw))
        return f
    return decorate


jinja_env = Env(loader=FileSystemLoader(Environment.templates_dir, ),
        bytecode_cache = FileSystemBytecodeCache(os.path.join(Environment.CONFIGPATH, 'cache'), '%s.cache'))
#url_map = Map([Rule('/theme/<file>', endpoint='theme', build_only=True)])
#url_map = Map([Rule('/robots.txt', endpoint='/robots.txt', build_only=True)])

#def url_for(endpoint, _external=False, **values):
    #return Environment.local.url_adapter.build(endpoint, values, force_external=_external)

#jinja_env.globals['url_for'] = url_for
jinja_env.globals['conf'] = Environment
#jinja_env.globals['a'] = 0

def render_template(template, **context):
    #print "Context", context
    return Response(jinja_env.get_template(template).render(**context),
                    mimetype='text/html')


def datetimeformat(value, format='%d/%m/%Y %H:%M '):
    if not value:
        return ""
    else:
        return value.strftime(format)

jinja_env.filters['datetimeformat'] = datetimeformat

def dateformat(value, format='%d/%m/%Y '):
    if not value:
        return ""
    else:
        return value.strftime(format)

jinja_env.filters['dateformat'] = dateformat

def bbcode(value):
    markup = create(annotate_links=False,target=True, use_pygments=False)
    if not value:
        return ""
    else:
        return markup(value)
jinja_env.filters['bbcode'] = bbcode


def noNone(value):
    if value =="None":
        return ""
    elif not value:
        return ""
    else:
        return value
jinja_env.filters['nonone'] = noNone


@environmentfilter
def url2href(environment, value):
    b = ""
    flag = True
    for a in value:
        if flag and a!="$":
            continue
        else:
            flag = False
            if a !="]":
                b += a
            flag = False
    value = '<a href =%s />%s</a>'  %(b.split(",")[0][5:], b.split(",")[1])
    return value

jinja_env.filters['url2href'] = url2href
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@environmentfilter
def nl2br(environment, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
                          for p in _paragraph_re.split(escape(value)))
    if environment.autoescape:
        result = Markup(result)
    return result
jinja_env.filters['nl2br'] = nl2br


class Request(BaseRequest):
    """Create a useful subclass of the base request that
    uses utf-8 internally."""
    charset = 'utf-8'

    def __init__(self, environ, url_adapter=None):
        BaseRequest.__init__(self, environ)
        #self.url_adapter = url_adapter

class Response(BaseResponse):
    """The same for the response object. Also set the default mimetype
    to ``text/html`` since this makes more sense for this example."""
    charset = 'utf-8'
    default_mimetype = 'text/html'

class RedirectResponse(Response):
    """Subclass of `Response` for simple redirecting."""

    def __init__(self, url):
        Response.__init__(self, 'Redirecting to %s...' % url,
                          mimetype='text/plain', status=302)
        self.headers['Location'] = url


class ManagePrint(object):

    def __init__(self, req, docType= None, report = None ):
        self.path = req.environ['PATH_INFO'].split('/')
        self._slaTemplate = Environment.templates_dir + self.path[1] +"/"+ Environment.sladir + docType + '.sla'
        self.pdfFolder = Environment.templates_dir + self.path[1] +"/"+ Environment.sladir
        self.report = report
        print self._slaTemplate

    def pdf(self, param):
        """ Restituisce una stringa contenente il report in formato PDF
        """
        #if self._slaTemplateObj is None:
        self._slaTemplateObj = Sla2Pdf(slaFileName=self._slaTemplate,
                                           pdfFolder=self.pdfFolder,
                                           report=self.report)

        param = param
        #param = []
        #for d in self.objects:
            #d.resolveProperties()
            #param.append(d.dictionary(complete=True))
        #print self._slaTemplateObj.serialize(param)
        return self._slaTemplateObj.serialize(param)


def renderizza(req,tpl,pageData):
    pageData["USER"] = getUserFromId(req)
    env = Env(loader=FileSystemLoader(Environment.CONFIGPATH +"/templates_email"))
    def noNone(value):
        if value =="None":
            return ""
        elif not value:
            return ""
        else:
            return value
    env.filters['nonone'] = noNone

    def dateformat(value, format='%d/%m/%Y '):
        if not value:
            return ""
        else:
            return value.strftime(format)

    env.filters['dateformat'] = dateformat
    tpl2 = env.get_template(tpl)
    html = tpl2.render(pageData=pageData)
    return html

def renderTemplate(pageData):
    #jinja_env.globals['environment'] = Environment
    jinja_env.globals['utils'] = utils
    pageData["titolo"] = pageData["file"].split(".")[0].capitalize()
    if "dao" in pageData:
        html = jinja_env.get_template("/"+pageData["file"]+".html").render(pageData = pageData, dao=pageData["dao"])
    else:
        html = jinja_env.get_template("/"+pageData["file"]+".html").render(pageData = pageData)
    return html




def subList():
    subss = Subdomain().select(batchSize=None)
    return subss


def addSlash(url=None):
    if url:
        return "/"+url
    else:
        return ""

def resizeImgThumbnail(name,req):
    """
    funzione di ridimensionamento immagine per la lista, di fatto
    crea un thumnail dell'immagine stessa
    """
    path = req.environ['PATH_INFO'].split('/')
    imageFile = Environment.artImagPath + name
    im1 = Image.open(imageFile)
    width = int(Environment.params[path[1]]['widthThumbnail'])
    height = int(Environment.params[path[1]]['heightThumbnail'])
    im5 = im1.resize((width, height), Image.ANTIALIAS)
    newname= 'thumb_'+ name
    im5.save(Environment.artImagPath + newname)
    #return data

def resizeImgDetail(name,req):
    """
    funzione di ridimensionamento immagine per la scheda
    dettaglio articolo chiamata medium size
    """
    path = req.environ['PATH_INFO'].split('/')
    imageFile = Environment.artImagPath + name
    im1 = Image.open(imageFile)
    width = int(Environment.params[path[1]]['widthdetail'])
    height = int(Environment.params[path[1]]['heightdetail'])
    im5 = im1.resize((width, height), Image.ANTIALIAS)
    newname= 'medium_'+ name
    im5.save(Environment.artImagPath + newname)
    #post_multipart(data)

def createRandomString(num=10):
    b = ""
    for c in range(num):
        a = random.choice('1234567890abcdefghilmnopqrstuvz')
        b = b + a
    return b


def hasAction(req=None, action=[], mark=""):
    """
    Importante il controllo se il ruolo è attivo
    se l'utente ha una sessione aperta ed ha i privilegi adeguati
    admin =  1,2,3,4,5
    utente = 1,2
    cliente = 1,2
    guest = 0
    """
    if Session(req).control():
        id_role = getIdRoleFromIdUser(req)
        ruol = Role().getRecord(id=id_role)
        if not ruol.active:
            return False
    else:
        test = Role().select(name="Guest")
        if test:
            id_role = test[0].id
        return False
    for act in action:
        can = RoleAction().select(id_role = id_role,
                                id_action=act,
                                batchSize=None)
        if not can:
            return False
    return True


def getRoleFromId(req):
    """
        ok ported to new pg2 Dao
    """
    idr = Session(req).getUserId()
    user = User(req=req).getRecord(id=idr)
    if user:
        id_role = user.id_role
        role = Role(req=req).getRecord(id=id_role)
        if not role.id:
            roleName = "Guest"
        else:
            roleName= role.name
    else:
        roleName = "Guest"
    return roleName

def getIdRoleFromIdUser(req):
    ids = Session(req).getUserId()
    if ids == 0:
        role = Role(req=req).select(name ="Guest")
        roleId = role[0].id
    else:
        role = User(req=req).getRecord(id=ids)
        roleId = role.id_role
    return roleId

def getIdlistinoFromRole(req):
    """
        ok ported to New Dao pg2
    """
    path = req.environ['PATH_INFO'].split('/')
    id_role = getIdRoleFromIdUser(req)
    if not id_role:
        listinoId = Environment.params[path[1]]['listinoDefault']
    else:
        role = Role(req).getRecord(id=id_role)
        listinoId = role.id_listino
    return listinoId

def getUserFromId(req):
    """
        ok, adattata ai nuovi Dao pG2
    """
    idrr = Session(req).getUserId()
    user = User(req=req).getRecord(id=idrr)
    if not user :
        return None
    else:
        return user

def getUsernameFromId(req):
    """
        ok, adattata ai nuovi Dao pG2
    """
    idrr = Session(req).getUserId()
    user = User(req=req).getRecord(id=idrr)
    if not user :
        return "Guest"
    else:
        return user.username

def includeFile(files, subdomain=None):
    """
        This search for the right template file in common or theme dir
    """
    print "files del template", files
    filename= files+'.html'
    pathFile = Environment.CONFIGPATH + '/templates/'
    if Environment.SUB:
        pathFilesub = pathFile+Environment.SUB.lower()+"/"

        if os.path.exists(str(pathFilesub+filename)):
            pathFilesub = Environment.SUB.lower()+"/"+filename
            return pathFilesub
    if os.path.exists(str(pathFile+filename)):
        pathFile = filename
        return pathFile
    else:
        pathFile = None
    return pathFile

def findAct(req):
    path = req.environ['PATH_INFO'].split('/')
    if req.form.get('act'):
        act = req.form.get('act')
    elif req.cookies.has_key(path[1]+'buy'):
        act = req.cookies[path[1]+'buy']
    elif req.cookies.has_key('reg'):
        act = req.cookies['reg']
    else:
        act = None
    return act


def resizeImgThumbnailGeneric(req=None, name=None):
    """
    funzione di ridimensionamento immagine per la lista, di fatto
    crea un thumnail dell'immagine stessa
    """
    path=req.environ['PATH_INFO'].split('/')
    nameuser = getUsernameFromId(req)
    envtDir = Environment.configPath+"style/" +path[1]+"/data/"+nameuser+"/images"
    imageFile = envDir +"/"+name
    im1 = Image.open(imageFile)
    width = int(Environment.params[path[1]]['widthThumbnail'])
    height = int(Environment.params[path[1]]['heightThumbnail'])
    im5 = im1.resize((width, height), Image.ANTIALIAS)
    newname= 'thumb_'+ name
    im5.save(envDir +"/"+ newname)


def prepareUserEnv(req):
    nameuser = getUsernameFromId(req)
    envDir = Environment.CONFIGPATH+"/templates/media/" +nameuser+"/"+"images"
    if not (os.path.exists(envDir)):
        os.makedirs(envDir)
    return envDir

def checkPath(path=None, correctPath=None):
    for a in correctPath:
        if a not in path:
            return False
    return True

def getCategorieContatto(id=None):
    from core.dao.ContattoCategoriaContatto import ContattoCategoriaContatto
    dbCategorieContatto = ContattoCategoriaContatto().select(id=id,
                                                            batchSize=None)
    return dbCategorieContatto

def getRecapitiContatto(id=None):
    from core.dao.RecapitoContatto import RecapitoContatto
    dbRecapitiContatto = RecapitoContatto().select(idContatto=id)
    return dbRecapitiContatto

def getfeedFromSite(name=None, items=3):
    string = ""
    #if Environment.feedAll == "":
    feedToHtml = []
    try:
        feed=Feed().select(name=name)[0]
        feedurl = feed.url
        d = feedparser.parse(feedurl)
        feedList = d['entries']
        for feed in feedList[:items]:
            try:
                body = feed['content'][0]['value']
            except:
                body = feed["summary_detail"]['value']
            feed = {
                "title" :feed['title'],
                "links": feed['links'][0]['href'],
                "body" : body,
                "updated" : feed['updated'][4:-14],
                "autore" : feed['author']
                }
            feedToHtml.append(feed)
        #Environment.feedCache = feedToHtml
        #self.renderPage(feedToHtml)
        return feedToHtml
    except:
        feed = {
                "title" : "",
                "links":  "",
                "body" :  "",
                "updated" :  "",
                "autore" :  ""
                }
        feedToHtml.append(feed)
        return feedToHtml

def permalinkaTitle(string):
    import unicodedata
    string = unicodedata.normalize("NFKD",string).encode('ascii','ignore').strip().lower()
    test = "-".join(string.split())
    badchar = []
    for char in test:
        if char not in "qwertyuiopasdfghjklzxcvbnm1234567890-_":
            badchar.append(char)
    if badchar:
        for ch in badchar:
            test = test.replace(str(ch),"")
    return test


def pagination(req,batch,count):
    pag  = req.args.get('pag')
    pages = req.args.get('pages')
    searchkey= req.form.get('searchkey')
    args = req.args.to_dict()
    if not searchkey:
        searchkey= req.args.get('searchkey')
    if not pag:
        pag = 1
    else:
        pag = int(pag)
    if pag < 2:
        offset = 0
    else:
        offset = (int(pag)*batch)-batch
    if not pages or searchkey :
        if count:
            pages = int(math.ceil(float(count)/float(batch)))
        else: pages = 1
    args["pages"] = pages
    args["pag"] = pag
    args["searchkey"] = searchkey
    args["count"] = count
    args["offset"] = offset
    return args


def createcaptcha():
    img = Image.new("RGB", (220, 75), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    pathFile = Environment.CONFIGPATH
    font = ImageFont.truetype(pathFile+"/Trash_.ttf", 52)
    r,g,b = rint(0,255), rint(0,255), rint(0,255)
    dr = (rint(0,255) - r)/300.
    dg = (rint(0,255) - g)/300.
    db = (rint(0,255) - b)/300.
    for i in range(300):
        r,g,b = r+dr, g+dg, b+db
        draw.line((i,0,i,300), fill=(int(r),int(g),int(b)))
    string = ""
    values = "23456789QWERTYUPASDFGHJKLZXCVBNMabcdefghmnpqrstuvz"
    for a in range(5):
        b =  rint(0,35)
        string += values[b]
    draw.text((20, 20), string, font=font)
    img.save(pathFile+"/templates/captcha.png", "PNG")
    return string

def setconf(key):
    """ Importante funzione che "semplifica" la lettura dei dati dalla tabella
    di configurazione setconf
    Tentativo abbastanza rudimentale per gestire le liste attraverso i ; ma
    forse si potrebbero gestire più semplicemente con le virgole
    """
    conf = SetConf().select(key=key)
    c = []
    if conf:
        if ";" in str(conf[0].value):
            val = str(conf[0].value).split(";")
            for a in val:
                c.append(a.strip())
            return c
        else:
            return str(conf[0].value)
    else:
        return ""

def dateToString(data):
    """
    Converte una data in stringa
    """
    if data is None:
        return ''
    elif type(data) == str:
        return data
    else:
        try:
            s = string.zfill(str(data.day),2) + '/' + string.zfill(str(data.month),2) + '/' + string.zfill(str(data.year),4)
        except Exception:
            s = ''
        return s

def dateTimeToString(data):
    """
    Converte una data + ora in stringa
    """
    if data is None:
        return ''
    elif type(data) == str:
        return data
    else:
        try:
            s = string.zfill(str(data.day), 2) + '/' + string.zfill(str(data.month),2) + '/' + string.zfill(str(data.year),4) + ' ' + string.zfill(str(data.hour),2) + ':' + string.zfill(str(data.minute),2)
        except Exception:
            s = ''
        return s

def subdoms():
    ssdict = {}
    sds = Subdomain().select(batchSize=None)
    for s in sds:
        ssdict[str(s.name).lower()] = s
    return ssdict

def getRecapitiContatto(id=None):
    """
    """
    from promogest.dao.RecapitoContatto import RecapitoContatto
    if id:
        dbRecapitiContatto = RecapitoContatto().select(idContatto=id)
    else:
        dbRecapitiContatto = []
    return dbRecapitiContatto


def getRecapitiCliente(idCliente):
    """Dato un cliente restituisce un dizionario dei recapiti"""
    from promogest.dao.ContattoCliente import ContattoCliente
    from promogest.dao.RecapitoContatto import RecapitoContatto
    recaCli = {}
    cc = ContattoCliente().select(idCliente=idCliente)
    if cc:
        reca = RecapitoContatto().select(idContatto=cc[0].id,  batchSize=None)
        return reca
    return []


def getRecapitiFornitore(idFornitore):
    """Dato un cliente restituisce un dizionario dei recapiti"""
    from promogest.dao.ContattoFornitore import ContattoFornitore
    from promogest.dao.RecapitoContatto import RecapitoContatto
    recaCli = {}
    cc = ContattoFornitore().select(idFornitore=idFornitore)
    if cc:
        reca = RecapitoContatto().select(idContatto=cc[0].id,  batchSize=None)
        return reca
    return []



def codeIncrement(value):
    """
    FIXME
    @param value:
    @type value:
    """

    lastNum = re.compile(r'(?:[^\d]*(\d+)[^\d]*)+')

    def increment(s):
        """ look for the last sequence of number(s) in a string and increment """
        m = lastNum.search(s)
        if m:
            next = str(int(m.group(1))+1)
            start, end = m.span(1)
            s = s[:max(end-len(next), start)] + next + s[end:]
            return s

    return increment(value)


def setconf(section, key, value=False):
    """ Importante funzione che "semplifica" la lettura dei dati dalla tabella
    di configurazione setconf
    Tentativo abbastanza rudimentale per gestire le liste attraverso i ; ma
    forse si potrebbero gestire più semplicemente con le virgole
    """
    if Environment.tipo_eng =="postgresql" or Environment.tipo_eng =="postgres" :
        if not hasattr(Environment.conf, "Documenti"):
            Environment.conf.add_section("Documenti")
            Environment.conf.save()
        if  hasattr(Environment.conf, "Documenti") and not hasattr(Environment.conf.Documenti, "cartella_predefinita"):
            setattr(Environment.conf.Documenti,"cartella_predefinita",Environment.documentsDir)
            Environment.conf.save()
        if key == "cartella_predefinita":
            return Environment.conf.Documenti.cartella_predefinita
    from promogest.dao.Setconf import SetConf
    confList = Environment.confList
    if not confList:
        confList = SetConf().select(batchSize=None)
        Environment.confList = confList

    confff = None
    for d in confList:
        if not value:
            if d.key==key and d.section==section:
                confff = d
                break
        else:
            if d.key==key and d.section==section and d.value == value:
                confff = d
                break
    if not confff:
        if not value:
            confff = SetConf().select(key=key, section=section)
        elif value:
            confff = SetConf().select(key=key, section=section, value=value)
        if confff:
            confff = confff[0]
    c = []
    if confff:
        valore = confff.value
        if ";" in str(valore):
            val = str(valore).split(";")
            for a in val:
                c.append(a.strip())
            return c
        else:
            if valore == "":
                return None
            elif valore and len(valore.split("/"))>=2:
                return str(valore)
            else:
                try:
                    return eval(valore)
                except:
                    return str(valore)

    else:
        return ""



nationList=["Afganistan","Albania","Algeria","Arabia Saudita","Argentina","Australia",
            "Austria","Belgio","Bermude","Bielorussia","Bolivia","Bosnia-Erzegovina","Brasile",
            "Bulgaria","Canada","Ceca (Repubblica)","Cile","Cina","Cipro","Colombia","Corea del Sud",
            "Costarica","Croazia","Cuba","Danimarca","Egitto","Estonia","Filippine","Finlandia",
            "Francia","Georgia","Germania","Giappone","Gran Bretagna","Grecia","Hong Kong","India",
            "Indonesia","Iran","Iraq","Irlanda","Islanda","Israele","Italia","Kazakstan","Kuwait","Lettonia",
            "Libano","Libia","Lituania","Lussemburgo","Malta","Marocco","Messico","Monaco","Montenegro",
            "Norvegia","Nuova Zelanda","Paesi Bassi", "Peru`","Polonia","Portogallo","Regno Unito","Romania",
            "Russia (Federazione)","S.Marino","Senegal","Serbia (Repubblica)","Siria","Slovacca (Repubblica)",
            "Slovenia","Somalia","Spagna","Stati Uniti d'America","Sudafrica","Svezia","Svizzera","Tailandia",
            "Taiwan","Tunisia","Turchia","Ucraina","Ungheria","Unione Europea","Uruguay","Vaticano","Venezuela",
            "Vietnam"]
