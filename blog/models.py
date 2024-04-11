from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

#each class is a subclass of models.Model
class Post(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset(). filter(status='published')


    options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish_date')
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=50, choices=options, default='draft')
    objects = models.Manager() #default manager
    newmanager = NewManager() #custom manager

    #to order posts on the basis of there time
    class Meta:
        ordering = ('-publish_date',)

    def get_absolute_url(self):
            return reverse("blog:post_single", args={self.slug})
    

    #to return the title of blog on admin panel else it shows post_object1, 2...
    def __str__(self):
        return self.title
