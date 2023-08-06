# Copyright 2014-2015 Rumma & Ko Ltd
# License: BSD, see LICENSE for more details.

"""
Overrides :mod:`lino_xl.lib.contacts` for :mod:`lino.projects.min2`.

.. autosummary::
   :toctree:

   models

"""

from lino_xl.lib.contacts import Plugin


class Plugin(Plugin):

    extends_models = ['Partner', 'Person', 'Company']
    use_vcard_export = True
