# -*- coding: iso-8859-15 -*-

# Promogest
#
# Copyright (C) 2005-2008 by Promotux Informatica - http://www.promotux.it/
# Author: Alceste Scalas <alceste@promotux.it>
# Author: Francesco Meloni <francesco@promotux.it>


import gtk

from ErrorDialog import ErrorDialog
from FatalErrorDialog import FatalErrorDialog

from promogest.lib.ExceptionHandler import ExceptionHandler

from promogest.dao.DataIntegrityException import DataIntegrityException
from ApplicationException import ApplicationException as DBApplicationException


from promogest.lib.sqlalchemy.exc  import IntegrityError as pgIntegrityError
from promogest.lib.sqlalchemy.exc import ProgrammingError as pgProgrammingError

class GtkExceptionHandler(ExceptionHandler):
    """ Exception handler that shows exceptions in a GTK window """

    def handle(self, exception):
        if isinstance(exception, (DataIntegrityException,
                                  pgProgrammingError)):
            dialog = FatalErrorDialog(message=str(exception))
        elif isinstance(exception, (DBApplicationException,
                                    pgIntegrityError)):
            dialog = ErrorDialog(message=str(exception))
        else:
            # Let's not die if we don't know what to do
            dialog = ErrorDialog(message=str(exception))
