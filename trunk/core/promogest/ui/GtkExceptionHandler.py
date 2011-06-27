# -*- coding: utf-8 -*-

#    Copyright (C) 2005, 2006, 2007 2008, 2009, 2010 by Promotux
#                        di Francesco Meloni snc - http://www.promotux.it/

#    Author: Francesco Meloni  <francesco@promotux.it>
#    Author: Andrea Argiolas  <andrea@promotux.it>
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


from ErrorDialog import ErrorDialog
from FatalErrorDialog import FatalErrorDialog

from promogest.lib.ExceptionHandler import ExceptionHandler

from promogest.dao.DataIntegrityException import DataIntegrityException
from ApplicationException import ApplicationException as DBApplicationException


from sqlalchemy.exc  import IntegrityError as pgIntegrityError
from sqlalchemy.exc import ProgrammingError as pgProgrammingError

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
