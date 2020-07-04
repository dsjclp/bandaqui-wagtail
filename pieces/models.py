from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from wagtail.snippets.models import register_snippet
from taggit.models import Tag

from .abstract import (
    PieceCategoryAbstract,
    PieceCategoryPiecePageAbstract,
    PieceIndexPageAbstract,
    PiecePageAbstract,
    PiecePageTagAbstract
)


COMMENTS_APP = getattr(settings, 'COMMENTS_APP', None)


class PieceIndexPage(PieceIndexPageAbstract):
    class Meta:
        verbose_name = _('Piece index')

    @property
    def pieces(self):
        # Get list of piece pages that are descendants of this page
        pieces = PiecePage.objects.descendant_of(self).live()
        pieces = pieces.order_by(
            '-date'
        ).select_related('owner').prefetch_related(
            'tagged_items__tag',
            'categories',
            'categories__category',
        )
        return pieces

    def get_context(self, request, tag=None, category=None, author=None, *args,
                    **kwargs):
        context = super(PieceIndexPage, self).get_context(
            request, *args, **kwargs)
        pieces = self.pieces

        if tag is None:
            tag = request.GET.get('tag')
        if tag:
            pieces = pieces.filter(tags__slug=tag)
        if category is None:  # Not coming from category_view in views.py
            if request.GET.get('category'):
                category = get_object_or_404(
                    PieceCategory, slug=request.GET.get('category'))
        if category:
            if not request.GET.get('category'):
                category = get_object_or_404(PieceCategory, slug=category)
            pieces = pieces.filter(categories__category__name=category)
        if author:
            if isinstance(author, str) and not author.isdigit():
                pieces = pieces.filter(author__username=author)
            else:
                pieces = pieces.filter(author_id=author)

        # Pagination
        page = request.GET.get('page')
        page_size = 10
        if hasattr(settings, 'BLOG_PAGINATION_PER_PAGE'):
            page_size = settings.BLOG_PAGINATION_PER_PAGE

        paginator = None
        if page_size is not None:
            paginator = Paginator(pieces, page_size)  # Show 10 pieces per page
            try:
                pieces = paginator.page(page)
            except PageNotAnInteger:
                pieces = paginator.page(1)
            except EmptyPage:
                pieces = paginator.page(paginator.num_pages)

        context['pieces'] = pieces
        context['category'] = category
        context['tag'] = tag
        context['author'] = author
        context['COMMENTS_APP'] = COMMENTS_APP
        context['paginator'] = paginator
        context = get_piece_context(context)

        return context

    subpage_types = ['pieces.PiecePage']


@register_snippet
class PieceCategory(PieceCategoryAbstract):
    class Meta:
        ordering = ['name']
        verbose_name = _("Piece Category")
        verbose_name_plural = _("Piece Categories")


class PieceCategoryPiecePage(PieceCategoryPiecePageAbstract):
    class Meta:
        pass


class PiecePageTag(PiecePageTagAbstract):
    class Meta:
        pass


@register_snippet
class PieceTag(Tag):
    class Meta:
        proxy = True


def get_piece_context(context):
    """ Get context data useful on all piece related pages """
    context['authors'] = get_user_model().objects.filter(
        owned_pages__live=True,
        owned_pages__content_type__model='piecepage'
    ).annotate(Count('owned_pages')).order_by('-owned_pages__count')
    context['all_categories'] = PieceCategory.objects.all()
    context['root_categories'] = PieceCategory.objects.filter(
        parent=None,
    ).prefetch_related(
        'children',
    ).annotate(
        piece_count=Count('piecepage'),
    )
    return context


class PiecePage(PiecePageAbstract):
    class Meta:
        verbose_name = _('Piece page')
        verbose_name_plural = _('Piece pages')

    def get_piece_index(self):
        # Find closest ancestor which is a piece index
        return self.get_ancestors().type(PieceIndexPage).last()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['pieces'] = self.get_piece_index().pieceindexpage.pieces
        context = get_piece_context(context)
        context['COMMENTS_APP'] = COMMENTS_APP
        return context

    parent_page_types = ['pieces.PieceIndexPage']
