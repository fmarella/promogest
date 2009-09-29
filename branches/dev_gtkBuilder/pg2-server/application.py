#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# Janas 
#
# Copyright (C) 2005 by Promotux Informatica - http://www.promotux.it/
# Author: Francesco Meloni <francesco@promotux.it>

from werkzeug import script

def make_app():
    from application import PromoWeb
    return PromoWeb()

def make_shell():
    from shorty import models, utils
    application = make_app()
    return locals()

action_runserver = script.make_runserver(make_app, use_reloader=True)
#action_shell = script.make_shell(make_shell)
#action_initdb = lambda: make_app().init_database()
script.run()


#from genshi.template import TemplateLoader

#templates_dir=Environment.templates_dir
#loader = TemplateLoader([templates_dir])
#listSubDomain = os.listdir(Environment.domains)
#comandi Localizzazione
# pybabel extract -F ngs_mappingfile.ini ./ -o ngsresine.pot
# pybabel init -i ngsresine.pot -l en -d ./lang/
# pybabel compile -d ./lang/

#Environment.meta = MetaData().reflect(Environment.engine,schema=self.azienda )


class PromoWeb(object):

    def __init__(self, db_uri):
        local.application = self
        #self.database_engine = engine

    #def init_database(self):
        #meta
        ##metadata.create_all(self.database_engine)

    def __call__(self, environ, start_response):
        local.application = self
        request = Request(environ)
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
        except HTTPException, e:
            response = e
        return ClosingIterator(response(environ, start_response),
                               [session.remove, local_manager.cleanup])

#class MainApp(object):

    #def __init__(self):
        #local.application = self
        # setup the urls.

    #def index(self,req):
        #self.path = req.environ['PATH_INFO'].split('/')
        #print "OLLE", self.path
        ##tmpl = loader.load('index.html')

        ##stream = tmpl.generate(
                        ##path = self.path,
                        ##listSubDomain = listSubDomain)
        ##return Dispacer(req).index()
        ##return RedirectResponse("/pg2")

    #def subdomain(self,req, subdomain=None):
        #if subdomain in Environment.subdomain:
            ##Environment.subdomain = subdomain
            #print _("PROVA DI TRADUZIONE")
            #return Dispacer(req).index()
        #else:
            #return not_found(req)

    #def static(self,req,subdomain=None, page=None):
        ##print "staaaaaaaaaaaaaaaaaaaaaaaaaaaariccccccccccccccccccccccccc"
        #if subdomain in listSubDomain:
            #Environment.subdomain = subdomain
            #return Static(req).showPage(pageId=page)
        #else:
            #return not_found(req)

    #def section(self,req, subdomain=None, section=None):
        #if subdomain in Environment.subdomain:
            ##Environment.subdomain = subdomain
            #return Dispacer(req).index()
        #else:
            #return not_found(req)

    #def subsection(self,req, subdomain=None, section=None, subsection=None):
        #if subdomain in Environment.subdomain:
            #return Dispacer(req).index()
        #else:
            #return not_found(req)

    #def action(self, req, subdomain=None, section=None, subsection=None, action=None):
        #if subdomain in Environment.subdomain:
            #return Dispacer(req).index()
        #else:
            #return not_found(req)

    #def not_found(self,req):
        #"""  Called if no rule matches.
        #"""
        #return Response (u"<h1>Page Not Found Ricontrolla che l'url sia corretto</h1>")


#urls = Map([
    #Rule('/', endpoint=MainApp().index),
    #Rule('/Error', endpoint=MainApp().not_found),
    #Rule('/<subdomain>/', endpoint=MainApp().subdomain),
    #Rule('/<subdomain>/<section>', endpoint=MainApp().section),
    #Rule('/<subdomain>/<section>/', endpoint=MainApp().section),
    ##Rule('/<subdomain>/showPage/<page>', endpoint=MainApp().static),
    #Rule('/<subdomain>/<section>/<subsection>', endpoint=MainApp().subsection),
    #Rule('/<subdomain>/<section>/<subsection>/', endpoint=MainApp().subsection),
    #Rule('/<subdomain>/<section>/<subsection>/<action>', endpoint=MainApp().action),
    #Rule('/<subdomain>/<section>/<subsection>/<action>/', endpoint=MainApp().action)
    #])

#def not_found(req):
        #"""
        #Called if no rule matches.
        #"""
        #return Response(u"<h1>Page Not Found Ricontrolla che l'url sia corretto</h1>")


#def getLang(req):
    #"""
    #Legge l'userid dal file di sessione e lo restituisce
    #"""
    #try:
        #lang = req.cookies['ngsresinelangflagged']
    #except:
        #if "HTTP_ACCEPT_LANGUAGE" in req.environ:
            #lang=req.environ['HTTP_ACCEPT_LANGUAGE'][0:2]
        #else:
            #lang = "it"
##    finally:
##        lang='it'
    #return lang

#def setlang(req):
    #languages = getLang(req)
    ##loc = locale.getdefaultlocale()
    #lang = gettext.translation('messages', Environment.LANGPATH,languages=[languages] )
    #_ = lang.ugettext
    #lang.install()
    #return _

#url_map = Map()

#def expose(rule, **kw):
    #def decorate(f):
        #kw['endpoint'] = f.__name__
        #url_map.add(Rule(rule, **kw))
        #return f
    #return decorate

#def application(environ, start_response):
    #"""
    #The WSGI application that connects all together.
    #"""
    #Environment.local.url_adapter = Environment.url_map.bind_to_environ(environ)
    #req = Request(environ, Environment.local.url_adapter)
    ##setlang(req)
    ##try:
    #print "PPPPPPPPPPPPPPPPPP2", req.path
    #callback, args = Environment.local.url_adapter.match(req.path)
    ##except NotFound:
        ##resp = not_found(req)
    ##except RequestRedirect, e:
        ##resp = RedirectResponse(e.new_url)
    ##else:
        ##resp = callback(req, **args)
    #return resp(environ, start_response)


app = SharedDataMiddleware(PromoWeb, {
            '/theme': os.path.join(os.path.dirname(__file__), 'theme'),
            '/style': os.path.join(os.path.dirname(__file__), 'style')
            })
app2 = DebuggedApplication(app, evalex=True)

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    #_ = setlang(Environment.languages)
    run_simple( Environment.conf.Server.hostname,
                int(Environment.conf.Server.port),
                app2,
                use_reloader=True,
                extra_files=None,
                reloader_interval=1,
                threaded=True,
                processes=1,
                request_handler=None )
                #app)
