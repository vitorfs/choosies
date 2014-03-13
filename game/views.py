# coding: utf-8

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from game.models import Queue, Match, Move
from auth.forms import SignUpForm
from django.contrib.auth.decorators import login_required
import random

def home(request):
    if request.user.is_authenticated():
        context = RequestContext(request)
        return render_to_response('game/home.html', context)
    else:
        context = RequestContext(request,{'form': SignUpForm()})
        return render_to_response('auth/signup.html', context)

@login_required
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

@login_required
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

@login_required
def match(request, match_id):
    match = Match.objects.get(pk=match_id)
    if match.is_on_match(request.user):
        player_pick = match.get_moves()[0].player
        context = RequestContext(request, {'match': match, 'player_pick': player_pick})
        return render_to_response('game/match.html', context)
    else:
        redirect('/')

@login_required
def result(request, match_id):
    pass

@login_required
def check_queue_status(request):
    try:
        queue_id = request.POST['queue-id']
        queue = Queue.objects.get(pk=queue_id)
        if queue.status == Queue.MATCHED:
            match = Match.objects.get(queue__id=queue_id)
            return HttpResponse(match.id)
        else:
            return HttpResponse('-1')
    except:
        return HttpResponseBadRequest()

@login_required
def play(request):
    pass

@login_required
def pick_odd_or_even(request):
    try:
        match_id = request.POST['match-id']
        chosen_value = request.POST['pick-odd-or-even-input']
        if chosen_value in (Move.ODD, Move.EVEN):
            match = Match.objects.get(pk=match_id)
            if match.is_on_match(request.user):
                for move in match.get_moves():
                    if move.player.id == request.user.id:
                        move.choice = chosen_value
                    else:
                        if chosen_value == Move.ODD:
                            move.choice = Move.EVEN
                        else:
                            move.choice = Move.ODD
                    move.save()
                context = RequestContext(request, {'match': match})
                return render_to_response('game/partial_match.html', context)
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
    except:
        return HttpResponseBadRequest()