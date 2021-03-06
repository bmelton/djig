from django.conf.urls import patterns, include, url
from voting.views import vote_on_object

from tastypie.api import Api
from api import *
import signals

v1_api = Api(api_name='v1')
v1_api.register(NewsResource())

urlpatterns = patterns('',
    url(r'^$',                                          'djig.views.index',             name='djig_home'),
    url(r'^newest/$',                                   'djig.views.newest',            name='djig_newest'),
    url(r'^submit_link/$',                              'djig.views.submit_link',       name='djig_submit_link'),
    url(r'^submit_link_detail/$',                       'djig.views.submit_link_detail',name='djig_submit_link_detail'),
    url(r'^like/(?P<article_id>\d+)/$',                 'djig.views.like_article',      name='djig_like_article'),
    url(r'^article/(?P<slug>[-\w]+)/$',                 'djig.views.article_detail',    name='djig_article_detail'),
)
