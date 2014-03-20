# coding: utf-8

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from game.models import Queue, Match, Move
from auth.forms import SignUpForm
from django.contrib.auth.decorators import login_required
import random
from game.decorators import ajax_required, user_is_on_match

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
        queue = Queue.objects.filter(status=Queue.PENDING).exclude(player=request.user)[:1].get()
        queue.status = Queue.MATCHED
        queue.matched_player = request.user
        queue.save()

        match = Match(queue=queue)
        match.save()

        i = random.randint(0,1)

        player = Move(player=queue.player, match=match, pick_choice=(i==0))
        player.save()

        matched_player = Move(player=queue.matched_player, match=match, pick_choice=(i==1))
        matched_player.save()

        return redirect('/match/' + str(match.id) + '/picking/')
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
def match_pick(request, match_id):
    match = Match.objects.get(pk=match_id)
    if match.user_is_on_match(request.user):
        context = RequestContext(request, {'match': match})
        return render_to_response('game/match_picking.html', context)
    else:
        redirect('/')

@login_required
def match(request, match_id):
    match = Match.objects.get(pk=match_id)
    if match.user_is_on_match(request.user):
        context = RequestContext(request, {'match': match})
        return render_to_response('game/match.html', context)
    else:
        redirect('/')

@login_required
def result(request, match_id):
    match = Match.objects.get(pk=match_id)
    if match.user_is_on_match(request.user):
        context = RequestContext(request, {'match': match})
        return render_to_response('game/result.html', context)
    else:
        redirect('/')

@ajax_required
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

@ajax_required
@user_is_on_match
@login_required
def play(request):
    try:
        match_id = request.POST['match-id']
        value = int(request.POST['value'])
        if value in range(0,6):
            match = Match.objects.get(pk=match_id)
            if match.status == Match.RUNNING:
                finished = 0
                for move in match.get_moves():
                    if move.player.id == request.user.id and move.value == None:
                        move.value = value
                        move.save()
                    if move.value != None:
                        finished = finished + 1
                if finished == 2:
                    match.status = Match.FINISHED
                    match.winner = match.get_winner()
                    match.save()
                    return HttpResponse()
                else:
                    return HttpResponse('-1')
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
    except:
        return HttpResponseBadRequest()

@ajax_required
@user_is_on_match
@login_required
def pick_odd_or_even(request):
    try:
        match_id = request.POST['match-id']
        chosen_value = request.POST['pick-input']
        if chosen_value in (Move.ODD, Move.EVEN):
            match = Match.objects.get(pk=match_id)
            if match.status == Match.PICKING:
                for move in match.get_moves():
                    if move.player.id == request.user.id and move.pick_choice:
                        move.choice = chosen_value
                    else:
                        if chosen_value == Move.ODD:
                            move.choice = Move.EVEN
                        else:
                            move.choice = Move.ODD
                    move.save()
                match.status = Match.RUNNING
                match.save()
                return HttpResponse()
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
    except:
        return HttpResponseBadRequest()

@ajax_required
@user_is_on_match
@login_required
def check_pick_status(request):
    try:
        match_id = request.POST['match-id']
        match = Match.objects.get(pk=match_id)
        if match.status == Match.RUNNING:
            return HttpResponse(match.id)
        else:
            return HttpResponse('-1')
    except:
        return HttpResponseBadRequest()

@ajax_required
@user_is_on_match
@login_required
def check_result(request):
    try:
        match_id = request.POST['match-id']
        match = Match.objects.get(pk=match_id)
        if match.status == Match.FINISHED:
            return HttpResponse()
        else:
            return HttpResponse('-1')
    except:
        return HttpResponseBadRequest()

@login_required
def rank(request):
    users = User.objects.all()
    matches = Match.objects.filter(status=Match.FINISHED)
    rank_users = []
    for user in users:
        wins = 0
        matches_played = 0
        for match in matches:
            if match.winner.player.id == user.id:
                wins = wins + 1
            for move in match.get_moves():
                if user.id == move.player.id:
                   matches_played = matches_played + 1
                   break 
        if matches_played > 0:
            user.points = matches_played - (matches_played - wins)
            user.wins = wins
            user.matches_played = matches_played
            win_ratio = (float(wins)/float(matches_played)) * 100.0
            user.win_ratio = "{:2.2f}".format(win_ratio)
            rank_users.append(user)
    if rank_users:
        rank_users.sort(key=lambda u: u.points, reverse=True)
    context = RequestContext(request,{'users': rank_users})
    return render_to_response('game/rank.html', context)