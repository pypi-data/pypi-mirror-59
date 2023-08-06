from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt


class A(dd.Action):
    label = _("a")

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        return ar.success("Called a() on %s" % obj)



class Moo(dd.Model):
    a = A()

    def __str__(self):
        return '%s object' % (self.__class__.__name__)

    @dd.action(_("m"))
    def m(self, ar, **kw):
        return ar.success("Called m() on %s" % self)


class Moos(dd.Table):
    model = Moo

    b = A()

    @dd.action(_("t"))
    def t(obj, ar, **kw):
        return ar.success("Called t() on %s" % obj)


class S1(Moos):
    pass


class S2(Moos):
    a = None
    b = None
    m = None
    t = None
