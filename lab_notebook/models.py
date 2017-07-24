from __future__ import unicode_literals

from django.db import models

# Create your models here.
class LabNote(models.Model):
    note_title = models.CharField(max_length=50)
    note_date = models.DateField('date created')
    note_body = models.CharField(max_length=500)
    
    def __str__(self):
        return self.note_title
    
class LabResult(models.Model):
    # each result belongs to a note
    note_id = models.ForeignKey(LabNote, on_delete=models.CASCADE)
    absorbance = models.DecimalField(max_digits=4, decimal_places=3)
    concentration = models.DecimalField(max_digits=5, decimal_places=2)
    standard = models.BooleanField()
    
    def __str__(self):
        return "{}".format(self.note_id)