from django import template
from ..models import Post, Comments
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag()
def total_comments():
    return Comments.objects.filter(active=True).count()


@register.simple_tag()
def last_post_date():
    return Post.published.last().publish


@register.simple_tag()
def most_popular_posts(count=5):
    return Post.published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]


@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts
    }
    return context

# Add support for markdown as a template filter
@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))