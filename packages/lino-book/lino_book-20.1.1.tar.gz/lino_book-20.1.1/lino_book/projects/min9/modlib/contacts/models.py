# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
The `models` module for `lino.projects.min2.modlib.contacts`.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy

from lino.api import dd, rt

from lino_xl.lib.contacts.models import *
from lino.modlib.comments.mixins import Commentable
from lino_xl.lib.cal.workflows import feedback

# from lino_xl.lib.addresses.mixins import AddressOwner
from lino_xl.lib.dupable_partners.mixins import DupablePartner, DupablePerson


class Partner(Partner, mixins.CreatedModified, DupablePartner, Commentable):
    """A Partner as seen in `lino.projects.min2`.  It does not define any
    specific field but inherits from a specific set of mixins.

    """

    hidden_columns = 'created modified'

    # def get_overview_elems(self, ar):
    #     # In the base classes, Partner must come first because
    #     # otherwise Django won't inherit `meta.verbose_name`. OTOH we
    #     # want to get the `get_overview_elems` from AddressOwner, not
    #     # from Partner (i.e. AddressLocation).
    #     elems = super(Partner, self).get_overview_elems(ar)
    #     elems += AddressOwner.get_overview_elems(self, ar)
    #     return elems


class PartnerDetail(PartnerDetail):

    main = "general contact misc"

    general = dd.Panel("""
    overview:20 general2:20 general3:40
    reception.AppointmentsByPartner comments.CommentsByRFC
    """, label=_("General"))

    general2 = """
    id language
    url
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    address_box
    remarks:30
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    misc = dd.Panel("""
    created modified
    changes.ChangesByMaster
    """, label=_("Miscellaneous"))


class Person(Person, Partner, DupablePerson):
    """
    Represents a physical person.
    """

    class Meta(Person.Meta):
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        #~ ordering = ['last_name','first_name']

    @classmethod
    def get_user_queryset(cls, user):
        qs = super(Person, cls).get_user_queryset(user)
        return qs.select_related('country', 'city')

    def get_print_language(self):
        "Used by DirectPrintAction"
        return self.language

dd.update_field(Person, 'first_name', blank=False)
dd.update_field(Person, 'last_name', blank=False)


class PersonDetail(PersonDetail):

    main = "general contact misc"

    general = dd.Panel("""
    overview:20 general2:40 general3:40
    contacts.RolesByPerson:20 households.MembersByPerson:40 \
    humanlinks.LinksByHuman
    """, label=_("General"))

    general2 = """
    title first_name:15 middle_name:15
    last_name
    gender:10 birth_date age:10
    id language
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    #address_box addresses.AddressesByPartner
    remarks:30
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    misc = dd.Panel("""
    url
    created modified
    reception.AppointmentsByPartner
    """, label=_("Miscellaneous"))


class Persons(Persons):

    detail_layout = PersonDetail()


class Company(Company, Partner):
    """A company as seen in `lino.projects.min2`.

    .. attribute:: vat_id

        The VAT identification number.

    """
    class Meta:
        verbose_name = _("Organisation")
        verbose_name_plural = _("Organisations")

    vat_id = models.CharField(_("VAT id"), max_length=200, blank=True)


class CompanyDetail(CompanyDetail):

    main = "general contact notes misc"

    general = dd.Panel("""
    overview:20 general2:40 general3:40
    contacts.RolesByCompany
    """, label=_("General"))

    general2 = """
    prefix:20 name:40
    type vat_id
    url
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    #address_box addresses.AddressesByPartner
    remarks:30
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    notes = "notes.NotesByCompany"

    misc = dd.Panel("""
    id language
    created modified
    reception.AppointmentsByPartner
    """, label=_("Miscellaneous"))


class Companies(Companies):
    detail_layout = CompanyDetail()


# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     contacts = sender.modules.contacts

#     contacts.Partners.set_detail_layout(contacts.PartnerDetail())
#     contacts.Companies.set_detail_layout(contacts.CompanyDetail())


Partners.set_detail_layout(PartnerDetail())
Companies.set_detail_layout(CompanyDetail())
