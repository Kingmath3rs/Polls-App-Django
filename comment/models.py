from django.db import models

from poll.models import Poll
from user.models import User


class Comment(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    content = models.TextField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
