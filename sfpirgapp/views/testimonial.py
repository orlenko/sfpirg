from sfpirgapp.models import Testimonial
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from sfpirgapp.forms import TestimonialForm
from django.http.response import HttpResponseRedirect
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
import random
from sfpirgapp.templatetags.sfpirg_tags import _category_by_model
from django.conf import settings


def testimoniallist(request):
    testimonials = Testimonial.objects.all().order_by('-publish_date')
    paginator = Paginator(testimonials, 10)
    page = request.GET.get('page')
    try:
        aglist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        aglist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        aglist = paginator.page(paginator.num_pages)

    context = RequestContext(request, locals())
    return render_to_response('sfpirg/category.html', {}, context_instance=context)


def testimonial(request, slug):
    t = Testimonial.objects.get(slug=slug)
    page = t
    current_item = page.title
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/testimonial.html', {}, context_instance=context)


def add_testimonial(request):
    form = None
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            send_mail('New experience needing review', 'check it out: http://%s%s' % (request.META['SERVER_NAME'],
                                                                                      form.instance.get_absolute_url()),
                      'noreply@sfpirg.ca',
                      ['vlad@bjola.ca'],
                      fail_silently=settings.DEBUG)
            return HttpResponseRedirect('/')
    else:
        form = TestimonialForm(initial={'category': _category_by_model(Testimonial),
                                        'status': 1,
                                        '_order': 0,
                                        })
    current_item = 'Add Testimonial'
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/add_testimonial.html', {}, context_instance=context)


def random_testimonial(request):
    all_testimonials = Testimonial.objects.filter(status=CONTENT_STATUS_PUBLISHED)
    count = len(all_testimonials)
    if count:
        index = random.randint(0, count-1)
    testimonial = all_testimonials[index]
    return HttpResponseRedirect('/testimonial/%s' % testimonial.slug)
