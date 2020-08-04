from django.db import models

from wagtail.core.models import Page, Orderable, Collection
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel,
)
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class HomePage(Page):

    carouselimage1 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    carouseltext1 = RichTextField(blank=True, null=True)

    carouselimage2 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    carouseltext2 = RichTextField(blank=True, null=True)

    cardimage1 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    cardtext1 = RichTextField()

    cardimage2 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    cardtext2 = RichTextField()

    cardimage3 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    cardtext3 = RichTextField()

    invitation = RichTextField()



    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('carouseltext1', classname="full"),
        ImageChooserPanel('carouselimage1'),
        FieldPanel('carouseltext2', classname="full"),
        ImageChooserPanel('carouselimage2'),
        FieldPanel('cardtext1', classname="full"),
        ImageChooserPanel('cardimage1'),
        FieldPanel('cardtext2', classname="full"),
        ImageChooserPanel('cardimage2'),
        FieldPanel('cardtext3', classname="full"),
        ImageChooserPanel('cardimage3'),
        FieldPanel('invitation', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        next_event = EventCalPage.objects.filter(start_dt__gte=timezone.now(), categories__slug='public').order_by('start_dt').first()
        context['nextevent'] = next_event
        return context

from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey

from django.conf import settings
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = settings.AUTH_USER_MODEL

from location_field.models.plain import PlainLocationField

from wagtail.snippets.edit_handlers import SnippetChooserPanel

@register_snippet
class Instrument(models.Model):  
    INSTRUMENT_CHOICES = [
        ('Instrument non précisé', 'Instrument non précisé'),
        ('Clarinette sib solo', 'Clarinette sib solo'),
        ('Clarinette mib', 'Clarinette mib'),
        ('Clarinette sib 1', 'Clarinette sib 1'),
        ('Clarinette sib 2', 'Clarinette sib 2'),
        ('Clarinette sib 3A', 'Clarinette sib 3A'),
        ('Clarinette sib 3B', 'Clarinette sib 3B'),
        ('Clarinette sib 4', 'Clarinette sib 4'),
        ('Clarinette sib 5', 'Clarinette sib 5'),
        ('Clarinette basse 1A', 'Clarinette basse 1A'),
        ('Clarinette basse 1B', 'Clarinette basse 1B'),
        ('Clarinette basse 2', 'Clarinette basse 2'),
        ('Clarinette alto', 'Clarinette alto'),
        ('Cor de basset', 'Cor de basset'),
        ('Contrebasse à cordes', 'Contrebasse à cordes'),
        ('Trompette', 'Trompette'),
        ('Caisse claire', 'Caisse claire'),
        ('Grosse caisse', 'Grosse caisse'),
        ('Saxophone alto', 'Saxophone alto'),
        ('Saxophone baryton', 'Saxophone baryton'),
         ('Saxophone soprano', 'Saxophone soprano'),
        ('Saxophone ténor', 'Saxophone ténor'),
        ('Soubassophone', 'Soubassophone'),
        ('Trombone', 'Trombone')
    ]
    title = models.CharField(max_length=200,
        choices=INSTRUMENT_CHOICES,default='Clarinette sib')
    class Meta:
        ordering = ('title',)
    
    panels = [
        FieldPanel('title'),
    ]

    def __str__(self):
        return self.title

@register_snippet
class Participation(models.Model):
    event_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    PARTICIPATION_CHOICES = [
    ('OUI', 'J y serai'),
    ('NON', 'Je n y serai pas'),
    ('PEUT-ETRE', 'Je ne suis pas sûr'),  
    ]
    choice = models.CharField(max_length=9,choices=PARTICIPATION_CHOICES, default='OUI')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='instrumentparticipations')
    iswaiting = models.BooleanField('is waiting status', default=False)
    
    class Meta:
        ordering = ('instrument',)
        verbose_name = u'Inscription'
        verbose_name_plural = u'Inscriptions'

    def __str__(self):
        return '%s %s %s %s' % (self.event_page,self.instrument,self.user,self.choice)

@register_snippet
class Video(models.Model):
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255)

    panels = [
        FieldPanel('titile'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

@register_snippet
class Trombipiece(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    panels = [
        FieldPanel('user', classname='full'),
        ImageChooserPanel('image'),
    ]

    def __str__(self):
        return self.user.first_name

class AboutPage(Page):

    heading = models.CharField(max_length=65)
    subheading = models.CharField(max_length=65)
    
    cardimage1 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    cardtext1 = RichTextField()

    invitation = RichTextField()
  

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('subheading', classname="full"),
        FieldPanel('cardtext1', classname="full"),
        ImageChooserPanel('cardimage1'),
        FieldPanel('invitation', classname="full"),
    ]

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from django.shortcuts import redirect


from events.models import EventCalPage
from .blocks import HeadingBlock
from .blocks import BaseStreamBlock

class TeamPage(Page):

    heading = models.CharField(max_length=65)
    subheading = models.CharField(max_length=65)
    
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    info = RichTextField()

    body = StreamField(
        BaseStreamBlock(), verbose_name="Body", blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('subheading', classname="full"),
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        FieldPanel('info', classname="full"),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        context = super(TeamPage, self).get_context(request)
        next_event = EventCalPage.objects.filter(start_dt__gte=timezone.now(), categories__slug='public').order_by('start_dt').first()
        context['nextevent'] = next_event
        return context

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

class FormPage(AbstractEmailForm):

    heading = models.CharField(max_length=65)
    subheading = models.CharField(max_length=65)
    body = StreamField(BaseStreamBlock())
    thank_you_text = models.TextField(
        help_text='Remerciements',
        blank=True)

    # Note how we include the FormField object via an InlinePanel using the
    # related_name value
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('subheading', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]


from django import forms

from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail_blocks.blocks import HeaderBlock, ListBlock, ImageTextOverlayBlock, CroppedImagesWithTextBlock, \
    ListWithImagesBlock, ThumbnailGalleryBlock, ChartBlock, MapBlock, ImageSliderBlock
class BookPage(Page):
    book_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    body3 = StreamField([
        ('header', HeaderBlock()),
        ('list', ListBlock()),
        ('image_text_overlay', ImageTextOverlayBlock()),
        ('cropped_images_with_text', CroppedImagesWithTextBlock()),
        ('list_with_images', ListWithImagesBlock()),
        ('thumbnail_gallery', ThumbnailGalleryBlock()),
        ('chart', ChartBlock()),
        ('map', MapBlock()),
        ('image_slider', ImageSliderBlock()),
    ], blank=True)
    collection = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=['Root']),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Select the image collection for this gallery.'
    )

from wagtail.embeds.blocks import EmbedBlock
class VideosIndexPage(Page):

    heading = models.CharField(max_length=65)
    subheading = models.CharField(max_length=65)
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    body = StreamField([
        ('embedded_video', EmbedBlock(icon="media")),
    ], blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('subheading', classname="full"),
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
    ]