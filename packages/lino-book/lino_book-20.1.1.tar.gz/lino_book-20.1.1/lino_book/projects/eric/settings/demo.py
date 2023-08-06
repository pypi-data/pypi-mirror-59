# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Defines and instantiates a demo version of Lino riche."""

import datetime

from ..settings import *


class Site(Site):

    the_demo_date = datetime.date(2015, 5, 23)

    languages = "en de fr"
    # readonly = True
    
    # use_ipdict = True
    # use_websockets = True
    # default_ui = 'lino_extjs6.extjs6'

    def setup_plugins(self):
        """Change the default value of certain plugin settings.

        - :attr:`excerpts.responsible_user
          <lino_xl.lib.excerpts.Plugin.responsible_user>` is set to
          ``'jean'`` who is both senior developer and site admin in
          the demo database.

        """
        super(Site, self).setup_plugins()
        self.plugins.excerpts.configure(responsible_user='jean')
        if False:
            self.plugins.mailbox.add_mailbox(
                'mbox', "Luc's aaa mailbox", 
                '/home/luc/.thunderbird/luc/Mail/Local Folders/aaa')


SITE = Site(globals())

# SITE.plugins.extjs6.configure(theme_name='theme-classic')
# SITE.plugins.extjs6.configure(theme_name='theme-classic-sandbox')
# SITE.plugins.extjs6.configure(theme_name='theme-aria')
# SITE.plugins.extjs6.configure(theme_name='theme-grey')
# SITE.plugins.extjs6.configure(theme_name='theme-crisp')
# SITE.plugins.extjs6.configure(theme_name='theme-crisp-touch')
# SITE.plugins.extjs6.configure(theme_name='theme-neptune')
# SITE.plugins.extjs6.configure(theme_name='theme-neptune-touch')
# SITE.plugins.extjs6.configure(theme_name='theme-triton')
# SITE.plugins.extjs6.configure(theme_name='ext-theme-neptune-lino')

#in etc/aliases
# comments: /home/tonis/mbox
#SITE.plugins.inbox.configure(mbox_path='/home/tonis/mbox')
#SITE.plugins.inbox.configure(comment_reply_addr='comments@localhost')
DEBUG = True

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'

# SITE.update_settings(ALLOWED_HOSTS=["192.168.0.26","127.0.0.1"])
