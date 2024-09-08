from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse


# Define Custom Manager (optional) to filter queryset of published posts
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    # Define the class for choice text
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'R', 'Rejected'

    # Relations (user to posts)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')

    # Adding database fields
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250)
    # Date Fields (used jmodels from jalali library to convert the date and time to persian)
    publish = jmodels.jDateTimeField(default=timezone.now)
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    # Choices Field
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    # instantiate the custom manager for published posts (using jmanager to use jalali date library)
    # objects - models.Manager()
    objects = jmodels.jManager()
    published = PublishedManager()

    # Sorting based on publish field using Meta class and its indexing
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    # make an absolute path for an url to call in a template (Canonical URL)
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

    def __str__(self):
        return self.title