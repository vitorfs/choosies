# coding: utf-8

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from game.models import Queue, Match, Move

def home(request):
    context = RequestContext(request)
    return render_to_response('game/home.html', context)

def queue(request):
    try:
        queue = Queue.objects.filter(status=Queue.PENDING)[:1].get()
        queue.status = Queue.MATCHED
        queue.matched_player = request.user
        queue.save()
        match = Match(queue=queue)
        match.save()
        player = Move(player=queue.player, match=match, value=-1)
        player.save()
        matched_player = Move(player=queue.matched_player, match=match, value=-1)
        matched_player.save()
        return redirect('/match/' + str(match.id) + '/')
    except:
        queue = Queue(player=request.user)
        queue.save()
        context = RequestContext(request, {'queue': queue})
        return render_to_response('game/queue.html', context)

def cancel(request):
    try:
        queue_id = request.POST['queue-id']
        queue = Queue.objects.get(pk=queue_id)
        if queue.status == Queue.PENDING:
            queue.status = Queue.CANCELED
            queue.save()
    except:
        pass
    return redirect('/')

def match(request, match_id):
    context = RequestContext(request)
    return render_to_response('game/match.html', context)

def check_queue_status(request):
    try:
        queue_id = request.GET['queue-id']
        queue = Queue.objects.get(pk=queue_id)
        if queue.status == Queue.MATCHED:
            match = Match.objects.get(queue__id=queue_id)
            return HttpResponse(match.id)
        else:
            return HttpResponse('-1')
    except:
        return HttpResponseBadRequest()