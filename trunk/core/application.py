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
script.run()

class PromoWeb(object):

    def __init__(self, db_uri):
        local.application = self

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
