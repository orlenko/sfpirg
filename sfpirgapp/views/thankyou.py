from django.shortcuts import render_to_response
from django.template.context import RequestContext


def thankyou(request):
    thankyou = '''Thank you! Please check your email for a confirmation message.

    Check your spam folder if you don't see it. We will get back to you very soon.

<br/>
<br/>
~ The SFPIRG Team
    '''
    context = RequestContext(request, locals())
    return render_to_response('sfpirg/thankyou.html', {}, context_instance=context)