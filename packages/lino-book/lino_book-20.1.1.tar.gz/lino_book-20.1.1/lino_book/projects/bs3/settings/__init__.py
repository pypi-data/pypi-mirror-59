# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""The :xfile:`settings.py` modules for this variant.

It has :attr:`default_user<lino.core.site.Site.default_user>` set to
'anonymous', which causes it to deactivate both authentication and
sessions.

.. autosummary::
   :toctree:

   demo
   doctests

"""


from lino_book.projects.team.settings.demo import *


class Site(Site):

    default_ui = 'lino.modlib.bootstrap3'
    # default_user = 'anonymous'

