from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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
    # Date Fields
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Choices Field
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    # instantiate the custom manager for published posts
    objects = models.Manager()
    published = PublishedManager()

    # Sorting based on publish field using Meta class and its indexing
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title