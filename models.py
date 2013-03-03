from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
import datetime
from uuslug import uuslug 

class Category(models.Model):
    title                   = models.CharField(max_length=100)
    slug                    = models.CharField(max_length=100, null=True, blank=True)
    image                   = models.URLField(null=True, blank=True)
    description             = models.TextField()

    class Meta():
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title

class Article(models.Model):
    title                   = models.CharField(max_length=100)
    slug                    = models.CharField(max_length=100, null=True, blank=True)
    url                     = models.URLField(null=True, blank=True)
    site                    = models.URLField(null=True, blank=True)
    site_name               = models.CharField(max_length=50, null=True, blank=True)
    self                    = models.NullBooleanField(default=False)
    description             = models.TextField(null=True, blank=True)
    image                   = models.URLField(null=True, blank=True)
    user                    = models.ForeignKey(User)
    category                = models.ForeignKey(Category, null=True, blank=True)
    created                 = models.DateTimeField(null=True, blank=True)
    love_count              = models.IntegerField(default=0)
    read_count              = models.IntegerField(default=0)
    comment_count           = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = uuslug(self.title, instance=self)
            self.created = datetime.datetime.now()
        super(Article, self).save(*args, **kwargs)

class ArticleFormLean(ModelForm):
    class Meta:
        model = Article
        exclude = ('title', 'slug', 'site', 'site_name', 'self', 'description', 'image', 'user', 'category', 
        'created', 'love_count', 'read_count', 'comment_count')

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ('slug', 'self', 'image', 'user', 'category', 'created', 'love_count',
        'read_count', 'comment_count')
