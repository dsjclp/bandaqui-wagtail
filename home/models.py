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


class HomePage(Page):

    carouselimage1 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    carouseltext1 = RichTextField()

    carouselimage2 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    carouseltext2 = RichTextField()

    carouselimage3 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    carouseltext3 = RichTextField()


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

    invitation = models.TextField(
        help_text='Invitation à la connexion',
        blank=True)
    

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('carouseltext1', classname="full"),
        ImageChooserPanel('carouselimage1'),
        FieldPanel('carouseltext2', classname="full"),
        ImageChooserPanel('carouselimage2'),
        FieldPanel('carouseltext3', classname="full"),
        ImageChooserPanel('carouselimage3'),
        FieldPanel('cardtext1', classname="full"),
        ImageChooserPanel('cardimage1'),
        FieldPanel('cardtext2', classname="full"),
        ImageChooserPanel('cardimage2'),
        FieldPanel('cardtext3', classname="full"),
        ImageChooserPanel('cardimage3'),
        FieldPanel('invitation', classname="full"),
    ]

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
class Partition(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField(blank=True)
    class Meta:
        ordering = ('title',)
        verbose_name = u'Partition'
        verbose_name_plural = u'Partitions'
    def __str__(self):
        return '%s' % (self.title)
    panels = [FieldPanel('title', classname='full'),FieldPanel('body', classname='full')]

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

    cardimage4 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) 

    cardtext4 = RichTextField()

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('cardtext1', classname="full"),
        ImageChooserPanel('cardimage1'),
        FieldPanel('cardtext2', classname="full"),
        ImageChooserPanel('cardimage2'),
        FieldPanel('cardtext3', classname="full"),
        ImageChooserPanel('cardimage3'),
        FieldPanel('cardtext4', classname="full"),
        ImageChooserPanel('cardimage4'),
    ]

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from django.shortcuts import redirect


from events.models import EventCalPage
from .blocks import HeadingBlock
from .blocks import BaseStreamBlock

class TeamPage(Page):
    
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
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        FieldPanel('info', classname="full"),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        context = super(TeamPage, self).get_context(request)
        context['nextevent'] = EventCalPage.objects.first()
        return context

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

class FormPage(AbstractEmailForm):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(BaseStreamBlock())
    thank_you_text = RichTextField(blank=True)

    # Note how we include the FormField object via an InlinePanel using the
    # related_name value
    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from modelcluster.fields import ParentalManyToManyField
from django import forms

class PartitionsIndexPage(Page):

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and '
        '3000px.'
    )
    partitions = ParentalManyToManyField('Partition', blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        MultiFieldPanel(
            [
                FieldPanel(
                    'partitions',
                    widget=forms.CheckboxSelectMultiple,
                ),
            ],
            heading="Partitions à mettre dans la liste",
        ),
    ]

    parent_page_types = ["TeamPage"]

    # Pagination for the index page. We use the `django.core.paginator` as any
    # standard Django app would, but the difference here being we have it as a
    # method on the model rather than within a view function
    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_breads(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

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
    partition = models.ForeignKey(
        'Partition',
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

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    body = StreamField([
        ('embedded_video', EmbedBlock(icon="media")),
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
    ]