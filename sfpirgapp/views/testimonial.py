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
from django.shortcuts import resolve_url
from mezzanine.utils.email import send_mail_template
from sfpirgapp.models import Settings


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
            testimonial = form.instance
            send_mail_template('New experience submitted: %s' % form.instance.title,
                   'sfpirg/email/experience_admin',
                   Settings.get_setting('SERVER_EMAIL'),
                   Settings.get_setting('ARX_ADMIN_EMAIL'),
                   context=locals(),
                   attachments=None,
                   fail_silently=settings.DEBUG,
                   addr_bcc=None)
            if form.cleaned_data.get('author_email'):
                send_mail_template('Your experience submitted: %s' % form.instance.title,
                       'sfpirg/email/experience_user',
                       Settings.get_setting('SERVER_EMAIL'),
                       form.cleaned_data.get('author_email'),
                       context=locals(),
                       attachments=None,
                       fail_silently=settings.DEBUG,
                       addr_bcc=None)
            return HttpResponseRedirect(resolve_url('thankyou'))
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
