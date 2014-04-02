from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from sfpirgapp.models import Category
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.db.models import Q
import datetime
from sfpirgapp.forms import ActionGroupFilterForm
from sfpirgapp.forms import ArxFilterForm


def get_arx_query_set(request, category):
    '''Show all ARX projects to admin,
    all organization's projects to the organization user,
    or published projects only to general public.'''
    user = request.user
    if user and not user.is_anonymous():
        if user.is_superuser:
            return category.arx_projects.all().order_by('pk', '-date_start')
        else:
            return category.arx_projects.filter(Q(is_approved=True, is_underway=False) | Q(user=user)).order_by('pk', '-date_start')
    else:
        return category.arx_projects.filter(is_approved=True, is_underway=False).order_by('pk', '-date_start')


def get_ag_query_set(request, category):
    '''Show published ActionGroup pages to everyone.
    Show all ActionGroup pages to admin.
    Show pending group page to the person who applied for it.
    '''
    user = request.user
    if user and not user.is_anonymous():
        if user.is_superuser:
            return category.action_groups.all().order_by('-publish_date')
        else:
            return category.action_groups.filter(Q(is_approved=True) | Q(user=user)).order_by('-publish_date')
    else:
        return category.action_groups.filter(is_approved=True).order_by('-publish_date')


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    kw = request.REQUEST
    filterform = None
    queryset = get_ag_query_set(request, category)
    if queryset:
        # TODO: add filters when we need them for Action Group
        #filterform = ActionGroupFilterForm(kw)
        #if filterform.is_valid():
        #    print 'Filtering: %s' % filterform.cleaned_data
        #    queryset = queryset.filter(**filterform.cleaned_data)
        #else:
        #    print 'Invalid filters! %s' % filterform.errors
        pass
    else:
        queryset = (category.testimonials.filter(status=2)
                or category.news_posts.filter(publish_date__lt=datetime.datetime.now()).order_by('-publish_date')
                or category.events.filter(start__gt=datetime.datetime.now()).order_by('start'))
    if not queryset:
        queryset = get_arx_query_set(request, category)
        filterform = ArxFilterForm(kw)
        if filterform.is_valid():
            print 'Filtering: %s' % filterform.cleaned_data
            if filterform.cleaned_data.get('project_type'):
                queryset = queryset.filter(project_type__in=filterform.cleaned_data['project_type'])
            if filterform.cleaned_data.get('project_subject'):
                queryset = queryset.filter(project_subject__in=filterform.cleaned_data['project_subject'])
        else:
            print 'Invalid filters! %s' % filterform.errors
    paginator = Paginator(queryset, 9)
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
