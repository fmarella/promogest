#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# Janas
#
# Copyright (C) 2009 by Promotux Informatica - http://www.promotux.it/


from werkzeug import run_simple
from werkzeug import script
from core import Environment
from werkzeug.debug import DebuggedApplication

def make_app():
    from Main import Janas
    application = DebuggedApplication(Janas(), evalex=True)
    return application

app = make_app()

if __name__ == '__main__':
    run_simple(hostname = Environment.conf.Server.hostname,
                    port = int(Environment.conf.Server.port),
                    application=app,
                    threaded = True,
                    #processes = 5,
                    use_reloader=True,
                    extra_files=["main.conf"]
    )

