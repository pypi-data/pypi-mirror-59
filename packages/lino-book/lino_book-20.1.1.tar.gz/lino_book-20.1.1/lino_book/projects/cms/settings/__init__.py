# -*- coding: UTF-8 -*-
# Copyright 2012-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""The Django settings module for Lino CMS.

"""

from lino.projects.std.settings import *


class Site(Site):

    verbose_name = "Lino CMS"
    version = "0.1"
    author = 'Rumma & Ko OÜ'
    author_email = 'luc@lino-framework.org'

    default_ui = 'lino_react.react'
    # default_ui = 'lino_xl.lib.pages'
    # admin_ui = 'lino.modlib.extjs'

    languages = 'en de fr'

    # project_model = 'tickets.Project'

    demo_fixtures = ['std', 'demo', 'demo2', 'intro']

    sidebar_width = 3

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.gfks'
        yield 'lino.modlib.extjs'
        yield 'lino.modlib.memo'
        # yield 'lino.modlib.bootstrap3'
        yield 'lino.modlib.users'
        yield 'lino.modlib.publisher'
        yield 'lino_xl.lib.countries'
        yield 'lino_xl.lib.contacts'
        #~ yield 'lino_xl.lib.outbox'
        yield 'lino_xl.lib.blogs'
        # yield 'lino.modlib.tickets'
        yield 'lino_xl.lib.pages'
        # yield 'lino_book.projects.cms'
