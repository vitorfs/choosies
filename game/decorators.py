from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from game.models import Match
from functools import wraps

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

def user_is_on_match(f):
    def wrap(request, *args, **kwargs):
        try:
            match_id = request.POST['match-id']
        except:
            return HttpResponseBadRequest()
        match = Match.objects.get(pk=match_id)
        if match.user_is_on_match(request.user):
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap