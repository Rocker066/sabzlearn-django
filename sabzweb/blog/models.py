import os
from datetime import datetime
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.template.defaultfilters import default
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify


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
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Choices Field
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    reading_time = models.PositiveIntegerField(verbose_name='زمان مطالعه')

    # instantiate the custom manager for published posts (using jmanager to use jalali date library)
    # objects - models.Manager()
    objects = models.Manager()
    published = PublishedManager()

    # Sorting based on publish field using Meta class and its indexing
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    # make an absolute path for an url to call in a template (Canonical URL)
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

    # Override the save method of the model to automatically generate slug using slugify
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)

    ## Another way to override delete method to delete all the images of a post when the post is deleted
    # def delete(self, *args, **kwargs):
    #     for img in self.images.all():
    #         storage, path = img.image_file.storage, img.image_file.path
    #         storage.delete(path)
    #     super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    message = models.TextField(max_length=250, verbose_name='پیام')
    name = models.EmailField(max_length=250, verbose_name='نام')
    email = models.EmailField(max_length=250, verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    subject = models.CharField(max_length=250, verbose_name='موضوع')

    class Meta:
        ordering = ['-message']
        indexes = [
            models.Index(fields=['-message']),
        ]
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return self.subject


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    name = models.CharField(max_length=250, verbose_name='نام')
    body = models.TextField(verbose_name='متن کامنت')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f'{self.name}: {self.post}'


class Image(models.Model):
    current_year = datetime.now().year
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='تصویر')
    # Using django-resized for modify images better
    image_file = ResizedImageField(upload_to=f'post_images/{current_year}', size=[500, 500], quality=100, crop=['middle', 'center'])
    title = models.CharField(max_length=250, verbose_name='عنوان', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'عکس'
        verbose_name_plural = 'عکس ها'

    # override delete method to delete all the images of a post when the post is deleted
    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else self.image_file.name


# Delete image files of the post from server when the post instance is deleted
@receiver(post_delete, sender=Image)
def delete_image_on_post_delete(sender, instance, **kwargs):
    """Delete image file from filesystem when the Image instance is deleted."""
    if instance.image_file:
        if os.path.isfile(instance.image_file.path):
            os.remove(instance.image_file.path)
