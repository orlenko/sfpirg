from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from news.models import NewsPost
from django.template.context import RequestContext
import datetime


def newslist(request):
    news = NewsPost.objects.filter(publish_date__lt=datetime.datetime.now()).order_by('-publish_date')
    paginator = Paginator(news, 10)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    context = RequestContext(request, locals())
    return render_to_response('sfpirg/newslist.html', {}, context_instance=context)


def newspost(request, news):
    newspost = get_object_or_404(NewsPost, slug=news)
    page = newspost
    context = RequestContext(request, locals())
    return render_to_response('pages/newspost.html', {}, context_instance=context)