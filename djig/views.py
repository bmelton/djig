from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests
from BeautifulSoup import BeautifulSoup
from models import Article, ArticleForm, ArticleFormLean
from urlparse import urlparse
from django.contrib.auth.decorators import login_required
from voting.models import Vote
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import date, timedelta
from text_utils import unescape
from voting.models import Vote
from django.views.decorators.csrf import csrf_exempt
from guardian.shortcuts import assign, remove_perm
from django.contrib.auth.models import Group, User

everybody_group = Group.objects.get(name="Everybody")

from django.conf import settings
if "actstream" in settings.INSTALLED_APPS:
    from actstream import action

COMMENTS_ENABLED = False
if "django.contrib.comments" in settings.INSTALLED_APPS:
    COMMENTS_ENABLED = True

def index(request):
    time_limit = date.today() - timedelta(hours=300)
    articleset = Article.objects.filter().order_by('-calculated_score')[:100]
    page = request.GET.get('page')
    paginator = Paginator(articleset, 10)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, "djig/index.html", {
        "articles"          : articles,
        "paginator"         : paginator,
        "page"              : page,
        "COMMENTS_ENABLED"  : COMMENTS_ENABLED,
    })

def newest(request):
    time_limit = date.today() - timedelta(hours=300)
    articleset = Article.objects.filter().order_by('-created')[:100]
    page = request.GET.get('page')
    paginator = Paginator(articleset, 10)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, "djig/index.html", {
        "articles"          : articles,
        "paginator"         : paginator,
        "page"              : page,
        "COMMENTS_ENABLED"  : COMMENTS_ENABLED,
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, "djig/detail.html", {
        "article"           : article,
        "COMMENTS_ENABLED"  : COMMENTS_ENABLED,
    })

@login_required
def submit_link(request):
    if request.method == "POST":
        form = ArticleFormLean(request.POST)
        if form.is_valid():
            url  = form.cleaned_data["url"]
            existing_article = Article.objects.filter(url=url)
            if existing_article.count() > 0:
                return HttpResponse("Duplicate")
            else:
                r = requests.get(url)
                soup = BeautifulSoup(r.text)
                title = unescape(soup.title.string)

                o = urlparse(url)
                site = "%s://%s" % (o.scheme, o.netloc)
                site_name = "%s" % o.netloc.replace("www.", "")
                data = {
                    'url': url, 
                    'title': title,
                    'site': site,
                    'site_name': site_name,
                }
                form = ArticleForm(initial=data)
                return render(request, "djig/submit_link.html", {
                    "form"          : form,
                })
        else:
            return HttpResponse(form.errors)
    else:
        form = ArticleForm()
        return render(request, "djig/submit_link.html", {
            "form"          : form,
        })

@login_required
def submit_link_detail(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            Vote.objects.record_vote(obj, request.user, +1)
            if "actstream" in settings.INSTALLED_APPS:
                action.send(request.user, verb='submitted', target=obj)
            return redirect("/")
        else:
            form = ArticleForm(request.POST)
            return render(request, "djig/submit_link.html", {
                "form"          : form,
            })
    else:
        return HttpResponse("You should POST to this page, not GET it.")
            

@csrf_exempt
@login_required
def like_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    Vote.objects.record_vote(article, request.user, +1)
    # article.love_count = article.love_count + 1
    # article.save()
    # article.calculate_score()
    if "actstream" in settings.INSTALLED_APPS:
        action.send(request.user, verb='liked', target=article)
    if request.method == "POST":
        return HttpResponse("{'result': 'success'}")
    else: 
        redirect_var = request.GET.get('next')
        if redirect_var:
            print redirect_var
            return redirect(redirect_var)
        else:
            return redirect("/")
