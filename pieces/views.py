from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from .models import PieceIndexPage, PiecePage, PieceCategory
from django.shortcuts import get_object_or_404
from django.conf import settings


def tag_view(request, tag):
    index = PieceIndexPage.objects.first()
    return index.serve(request, tag=tag)


def category_view(request, category):
    index = PieceIndexPage.objects.first()
    return index.serve(request, category=category)


def author_view(request, author):
    index = PieceIndexPage.objects.first()
    return index.serve(request, author=author)


class LatestEntriesFeed(Feed):
    '''
    If a URL ends with "rss" try to find a matching PieceIndexPage
    and return its items.
    '''

    def get_object(self, request, piece_slug):
        return get_object_or_404(PieceIndexPage, slug=piece_slug)

    def title(self, piece):
        if piece.seo_title:
            return piece.seo_title
        return piece.title

    def link(self, piece):
        return piece.full_url

    def description(self, piece):
        return piece.search_description

    def items(self, piece):
        num = getattr(settings, 'BLOG_PAGINATION_PER_PAGE', 10)
        return piece.get_descendants().order_by('-first_published_at')[:num]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.specific.body

    def item_link(self, item):
        return item.full_url

    def item_pubdate(self, piece):
        return piece.first_published_at


class LatestEntriesFeedAtom(LatestEntriesFeed):
    feed_type = Atom1Feed


class LatestCategoryFeed(Feed):
    description = "A Piece"

    def title(self, category):
        return "Piece: " + category.name

    def link(self, category):
        return "/piece/category/" + category.slug

    def get_object(self, request, category):
        return get_object_or_404(PieceCategory, slug=category)

    def items(self, obj):
        return PiecePage.objects.filter(
            categories__category=obj).order_by('-date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body