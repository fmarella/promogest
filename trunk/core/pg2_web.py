#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010, 2011 by Promotux
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

from werkzeug import run_simple
from werkzeug import script
from promogest import pg3_check
pg3_check.web = True
from promogest import Environment
from werkzeug.debug import DebuggedApplication

def make_app():
    from PgWeb import Pg2_web
    application = DebuggedApplication(Pg2_web(), evalex=True)
    return application

app = make_app()

if __name__ == '__main__':

    run_simple(hostname = Environment.webconf.Server.hostname,
                port = int(Environment.webconf.Server.port),
                application=app,
                threaded = True,
                #processes = 5,
                use_reloader=True,
                extra_files=["pgweb.conf", "templates_print"])
