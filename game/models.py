# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

class Queue(models.Model):
    PENDING = 'P'
    CANCELED = 'C'
    MATCHED = 'M'
    STATUS = (
        (PENDING, 'Pending'),
        (CANCELED, 'Canceled'),
        (MATCHED, 'Matched')
        )

    date = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey(User)
    matched_player = models.ForeignKey(User, null=True, related_name="matched_player")
    status = models.CharField(max_length=1, choices=STATUS, default=PENDING)

    class Meta:
        verbose_name = "Queue"
        verbose_name_plural = "Queues"
        ordering = ("date",)


class Match(models.Model):
    PICKING = 'P'
    RUNNING = 'R'
    CANCELED = 'C'
    FINISHED = 'F'
    STATUS = (
        (PICKING, 'Picking'),
        (RUNNING, 'Running'),
        (CANCELED, 'Canceled'),
        (FINISHED, 'Finished')
        )
    date = models.DateTimeField(auto_now_add=True)
    queue = models.ForeignKey(Queue)
    status = models.CharField(max_length=1, choices=STATUS, default=PICKING)
    winner = models.ForeignKey('Move', null=True, related_name='winner')

    def get_winner(self):
        moves = Move.objects.filter(match__id=self.id)
        odd = moves.filter(choice=Move.ODD).get()
        even = moves.filter(choice=Move.EVEN).get()

        if (odd.value + even.value) % 2 == 0:
            return even
        else:
            return odd

    def get_moves(self):
        moves = Move.objects.filter(match__id=self.id) 
        return moves

    def user_is_on_match(self, user):
        user_is_on_match = False
        for move in self.get_moves():
            if user.id == move.player.id:
                user_is_on_match = True
                break
        return user_is_on_match


class Move(models.Model):
    ODD = 'O'
    EVEN = 'E'
    CHOICES = (
        (ODD, 'Odd'),
        (EVEN, 'Even'),
        )

    player = models.ForeignKey(User)
    match = models.ForeignKey(Match)
    choice = models.CharField(max_length=1, choices=CHOICES)
    value = models.IntegerField(null=True)
    pick_choice = models.BooleanField()