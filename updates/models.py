import pytz
from django.db import models
from datetime import datetime 


class Record(models.Model):
    timestamp = models.DateTimeField()
    date = models.TextField()
    new_cases = models.TextField()

    def __str__(self):
        return '{}, {}, {}'.format(self.timestamp, self.date, self.new_cases)

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = datetime.now(pytz.timezone('America/Vancouver'))
        return super(Record, self).save(*args, **kwargs)
