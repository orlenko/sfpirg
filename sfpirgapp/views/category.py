from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from sfpirgapp.models import ActionGroup, Category
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    paginator = Paginator(category.action_groups.all()
                          or category.testimonials.all()
                          or category.news_posts.all()
                          or category.events.all(), 6)
    pagenum = request.GET.get('page')
    try:
        aglist = paginator.page(pagenum)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        aglist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        aglist = paginator.page(paginator.num_pages)
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/category.html', {}, context_instance=context)
