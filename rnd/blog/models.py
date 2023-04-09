from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]


class BlogPage(Page):
    author = models.CharField(max_length=254)
    description = models.CharField(max_length=254)
    body = RichTextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    search_fields = Page.search_fields + [
        index.SearchField('author'),
        index.SearchField('description'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('description'),
        FieldPanel('body'),
    ]