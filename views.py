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

def index(request):
    time_limit = date.today() - timedelta(hours=300)
    # current_articles = Article.objects.filter(created__gte=time_limit).order_by('-love_count', '-created')
    current_articles = Article.objects.filter().order_by('-love_count', '-created')
    articleset = Article.objects.filter().order_by('-love_count', '-created')
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
        "current_articles"  : current_articles,
        "paginator"         : paginator,
    })

def unescape(text):
    import re, htmlentitydefs
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text
    return re.sub("&#?\w+;", fixup, text)

@login_required
def submit_link(request):
    if request.method == "POST":
        form = ArticleFormLean(request.POST)
        if form.is_valid():
            url  = form.cleaned_data["url"]
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
            return HttpResponse("submit_link")
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
            return redirect("/")
        else:
            form = ArticleForm(request.POST)
            return render(request, "djig/submit_link.html", {
                "form"          : form,
            })
    else:
        return HttpResponse("You should POST to this page, not GET it.")
            

@login_required
def like_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    Vote.objects.record_vote(article, request.user, +1)
    article.love_count = article.love_count + 1
    article.save()
    return redirect("/")
