from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.


class PublishedManager(models.Manager):
    # override method to apply custom filter on the final QuerySet
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    # In order to use default manager and custom one they need to be explicitly created
    objects = models.Manager()  # The default manager
    published = PublishedManager()  # The custom manager. This will return post only with status='published'
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)

    # This field is intended to be used in URLs.
    # Slug is a short label contains only letters, numbers, underscores, hyphens.
    # Useful for building SEO-friendly URLs
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')

    # Many-to-One relationship key - one user can write many posts.
    # Here Django will create a foreign key using primary key of the related model
    # on_delete parameter specifies the behavior to adopt when te referenced object is deleted.
    # CASCADE means "When user is deleted - delete all his/her posts"
    # related_name helps to access related objects easily.
    # By this parameter reverse relationship (User to Post) is created
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)

    # time will be updated when saving an object
    updated = models.DateTimeField(auto_now=True)

    # values for this field can be chosen from STATUS_CHOICES tuple of tuples
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    tags = TaggableManager()

    # Post model contains metadata. Posts will be sorted descending by date published
    # Order specified with negative prefix (-)
    class Meta:
        ordering = ('-publish',)

    # human readable representation of an object
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    # Each post may has multiple comments - many-to-one relationships
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')  # override default comment_set name of relationship
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  # comment can be deactivated if inappropriate

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"

