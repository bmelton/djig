import datetime
from haystack import indexes
from models import Article
# from guardian.shortcuts import get_groups_with_perms

from django.contrib.auth.models import Group
everybody_group = Group.objects.get(name="Everybody")

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text        = indexes.CharField(document=True, use_template=True)
    author      = indexes.CharField(model_attr='user')
    created     = indexes.DateTimeField(model_attr='created')
    group_access= indexes.MultiValueField()

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())

    def get_updated_field(self):
        "created"

    def prepare_group_access(self, obj):
        return [everybody_group.pk]
        allowed_groups = []
        groups = Group.objects.filter(name='Everybody')
        for group in groups:
            allowed_groups.append(group.id)
        return allowed_groups
