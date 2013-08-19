from sfpirgapp.models import Testimonial
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def testimonial(request, slug):
    t = Testimonial.objects.get(slug=slug)
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/testimonial.html', {}, context_instance=context)