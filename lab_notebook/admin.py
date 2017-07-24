from django.contrib import admin

from .models import LabNote, LabResult

# Register your models here.
admin.site.register(LabNote)
admin.site.register(LabResult)