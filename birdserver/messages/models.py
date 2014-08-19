from django.db import models


class Message(models.Model):
    text = models.TextField()
    ackd = models.BooleanField(default=False)

    def __unicode__(self):
        return '{} ({}ackd)'.format(self.text, '' if self.ackd else 'un')
