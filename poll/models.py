import time
from django.db import models

from user.models import User


class PollManager(models.Manager):
    def countdown(self):
        t = self.time_left
        while (t):
            mins, secs = divmod(t, 60)
            time.sleep(1)
            t -= 1


class Poll(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    total_vote = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    time_left = models.DateTimeField()
    objects = PollManager()
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
