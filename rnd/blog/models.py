from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context        


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


class BlogPageImage(Orderable):
    # TODO: on_delete?, related_name? how?, ParentalKey?, Orderable class?
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='blog_page_image')

    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)
    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]