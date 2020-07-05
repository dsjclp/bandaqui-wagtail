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