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
        ordering = ("-date",)

class Match(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    queue = models.ForeignKey(Queue)

    def get_winner(self):
        moves = Move.objects.filter(match__id=self.id)
        odd = moves.filter(choice=Move.ODD).get()
        even = moves.filter(choice=Move.EVEN).get()

        if (odd.value + even.value) % 2 == 0:
            return odd.player
        else:
            return even.player


class Move(models.Model):
    ODD = 'O'
    EVEN = 'E'
    CHOICES = (
        (ODD, 'Odd'),
        (EVEN, 'Even'),
        )

    player = models.ForeignKey(User)
    choice = models.CharField(max_length=1, choices=CHOICES)
    value = models.IntegerField()
    match = models.ForeignKey(Match)