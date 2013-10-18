from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from sfpirgapp.models import Category
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.db.models import Q


def get_arx_query_set(request, category):
    '''Show all ARX projects to admin,
    all organization's projects to the organization user,
    or published projects only to general public.'''
    user = request.user
    if user and not user.is_anonymous():
        if user.is_superuser:
            return category.arx_projects.all()
        else:
            return category.arx_projects.filter(Q(is_approved=True, is_underway=False) | Q(user=user))
    else:
        return category.arx_projects.filter(is_approved=True, is_underway=False)


def get_ag_query_set(request, category):
    '''Show published ActionGroup pages to everyone.
    Show all ActionGroup pages to admin.
    Show pending group page to the person who applied for it.
    '''
    user = request.user
    if user and not user.is_anonymous():
        if user.is_superuser:
            return category.action_groups.all()
        else:
            return category.action_groups.filter(Q(is_approved=True) | Q(user=user))
    else:
        return category.action_groups.filter(is_approved=True)


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = (get_ag_query_set(request, category)
                or category.testimonials.all()
                or category.news_posts.all()
                or category.events.all()
                or get_arx_query_set(request, category))
    paginator = Paginator(queryset, 6)
    pagenum = request.GET.get('page')
    try:
        aglist = paginator.page(pagenum)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        aglist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        aglist = paginator.page(paginator.num_pages)
    current_item = category.title
    context = RequestContext(request, locals())
    template_name = 'sfpirg/category.html'
    if category.arx_projects.all():
        template_name = 'sfpirg/category_arx.html'
    if category.action_groups.all():
        template_name = 'sfpirg/category_ag.html'
    return render_to_response(template_name, {}, context_instance=context)
