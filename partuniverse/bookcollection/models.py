from __future__ import unicode_literals

from django.db import models

import partsmanagement

from django.utils.translation import ugettext_lazy as _
from polymorphic.models import PolymorphicModel


class Publisher(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=100,
        help_text=_("The name of the publisher")
    )
    place = models.CharField(
        _("Place"),
        max_length=100,
        help_text=_("The place, where the publisher publishes its"
                    " publications."),
        blank=True,
        null=True
    )

    def __unicode__(self):
        return (u'{}, {}'.format(self.name, self.place))

    class Meta:
        ordering = ['name', 'place']


class Person(models.Model):
    first_name = models.CharField(
        _("First name"),
        max_length=100,
        help_text=_("The first name of author"),
        null=True,
        blank=True
    )
    last_name = models.CharField(
        _("Last name"),
        max_length=100,
        help_text=_("The last name of the publisher."
                    "Or, if there is only one name.")
    )

    def __unicode__(self):
        return (u'{}, {}'.format(self.last_name, self.first_name))

    class Meta:
        ordering = ['last_name', 'first_name']


class Book(partsmanagement.models.Part):

    title = models.CharField(
        _("Title"),
        max_length=100,
        help_text=_("The title of a book."),
        null=False,
        blank=False,
        unique=True,
        default='No title'
    )
    subtitle = models.CharField(
        _("Subtitle"),
        max_length=250,
        help_text=_("The subtitle of a book if there is some"),
        null=True,
        blank=True
    )
    author = models.ManyToManyField(
        Person,
        related_name='+',
        verbose_name=_("Authors"),
        help_text=_("The list of authors of the book.")
    )
    translator = models.ManyToManyField(
        Person,
        related_name='+',
        verbose_name=_("Translators"),
        help_text=_("The list of translators of the book."),
        blank=True
    )
    publisher = models.ForeignKey(
        Publisher,
        verbose_name=_("Publisher"),
        help_text=_("The publisher of a book."),
        default=None
    )
    year = models.IntegerField(
        _('Publishing year'),
        help_text=_("The publishing year."),
        null=True,
        blank=True
    )
    isbn10 = models.CharField(
        _("ISBN-10"),
        max_length=13,
        blank=True,
        null=True
    )
    isbn13 = models.CharField(
        _("ISBN-13"),
        max_length=17,
        blank=True,
        null=True

    )
    language = models.CharField(
        _("Publishing language"),
        max_length=6,
        help_text=_("Language media is in. Use ISO-codes here."),
        blank=True,
        null=True
    )
    comment = models.TextField(
        _("Comment"),
        blank=True,
        null=True,
        max_length=200,
        help_text=_("A short conclusion.")
    )

    def __unicode__(self):
        return (u'{}').format(self.title)

    class Meta:
        ordering = ['title']
        unique_together = ("title", "isbn10", "isbn13")
