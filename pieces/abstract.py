from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel)
from wagtail.api import APIField
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

import datetime


class PieceIndexPageAbstract(Page):
    class Meta:
        verbose_name = _('Piece index')
        abstract = True


class PieceCategoryAbstract(models.Model):
    name = models.CharField(
        max_length=80, unique=True, verbose_name=_('Category Name'))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name="children",
        help_text=_(
            'Categories, unlike tags, can have a hierarchy. You might have a '
            'Jazz category, and under that have children categories for Bebop'
            ' and Big Band. Totally optional.'),
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name = _("Piece Category")
        verbose_name_plural = _("Piece Categories")

    panels = [
        FieldPanel('name'),
        FieldPanel('parent'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name


class PieceCategoryPiecePageAbstract(models.Model):
    category = models.ForeignKey(
        'PieceCategory',
        related_name="+",
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    page = ParentalKey('PiecePage', related_name='categories')
    panels = [
        FieldPanel('category'),
    ]


class PiecePageTagAbstract(TaggedItemBase):
    content_object = ParentalKey('PiecePage', related_name='tagged_items')

    class Meta:
        abstract = True



class PiecePageAbstract(Page):
    body = RichTextField(verbose_name=_('body'), blank=True)
    tags = ClusterTaggableManager(through='PiecePageTag', blank=True)
    date = models.DateField(
        _("Post date"), default=datetime.datetime.today,
        help_text=_("This date may be displayed on the Piece post. It is not "
                    "used to schedule posts to go live at a later date.")
    )
    header_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Header image')
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]
    Piece_categories = ParentalManyToManyField(
        'PieceCategory', through='PieceCategoryPiecePage', blank=True)

    settings_panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('go_live_at'),
                FieldPanel('expire_at'),
            ], classname="label-above"),
        ], 'Scheduled publishing', classname="publishing"),
        FieldPanel('date'),
    ]

    def get_absolute_url(self):
        return self.url

    class Meta:
        abstract = True
        verbose_name = _('Piece page')
        verbose_name_plural = _('Piece pages')
    
    api_fields = [APIField('body')]
    content_panels = [
        FieldPanel('title', classname="full title"),
        MultiFieldPanel([
            FieldPanel('tags'),
            FieldPanel('Piece_categories'),
        ], heading="Tags and Categories"),
        ImageChooserPanel('header_image'),
        FieldPanel('body', classname="full"),
    ]
