from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = BlogPage.objects.all().order_by('-created_at')
        # blogpages = self.get_children().live().order_by('-created_at')
        context['blogpages'] = blogpages
        return context        


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    author = models.CharField(max_length=254)
    description = models.CharField(max_length=254)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def main_image(self):
        gallery_item = self.blog_page_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None


    search_fields = Page.search_fields + [
        index.SearchField('author'),
        index.SearchField('description'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('description'),
        FieldPanel('body'),
        InlinePanel('blog_page_images', label="Images"),
        FieldPanel('tags'),
    ]


class BlogPageImage(Orderable):
    # TODO: on_delete?, related_name? how?, ParentalKey?, Orderable class?
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='blog_page_images')

    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)
    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


class BlogTagIndexPage(Page):

    def get_context(self, request):
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey('wagtailimages.Image',
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'blog categories'

