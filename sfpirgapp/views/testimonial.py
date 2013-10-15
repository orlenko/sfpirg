from sfpirgapp.models import Testimonial
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/testimonial.html', {}, context_instance=context)