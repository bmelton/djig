from django.contrib.auth.models import User
from django.conf.urls.defaults import url

from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from models import *

class NewsResource(ModelResource):
    class Meta:
        queryset        = Article.objects.filter()
        resource_name   = 'news'
        detail_uri_name = 'slug'

    def determine_format(self, request):
        return "application/json"

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d_.-]+)/$" % 
                self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
