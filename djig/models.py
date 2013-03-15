from django.db import models
from django.contrib.auth.models import User, Group
from django.forms import ModelForm
import datetime
from uuslug import uuslug 
import times
from django.utils.encoding import smart_unicode
from math import ceil
from guardian.shortcuts import assign, get_perms, get_groups_with_perms

everybody_group = Group.objects.get(name="Everybody")

class Category(models.Model):
    title                   = models.CharField(max_length=100)
    slug                    = models.CharField(max_length=100, null=True, blank=True)
    image                   = models.URLField(null=True, blank=True)
    description             = models.TextField()

    class Meta:
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
    calculated_score        = models.DecimalField(max_digits=10, decimal_places=10, default=0, null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        permissions = ( 
            ('group_view', 'Groups that can view'),
        ) 

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = uuslug(self.title, instance=self)
            self.title = self.title.encode("ascii", "ignore")
            self.created = datetime.datetime.now()
            assign('djig.group_view', everybody_group, self)
        super(Article, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('djig_article_detail', [self.slug])

    def calculate_score(self):
        now     = times.now()
        then    = times.to_universal(self.created)
        hour_age= ceil((now-then).total_seconds()/60/60)
        gravity = 1.8
        self.calculated_score = (self.love_count-1)/pow((hour_age+2), gravity)
        self.save()
        print "%s -- %s -- %s" % (self.calculated_score, hour_age, self.title)
        return (self.love_count-1) / pow((hour_age+2), gravity)

    def get_allowed_groups(self):
        allowed_groups = []
        groups = get_groups_with_perms(self, attach_perms=True)
        for group in groups.keys():
            if "group_view" in groups[group]:
                allowed_groups.append(group)
        return allowed_groups

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
