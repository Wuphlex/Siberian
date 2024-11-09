from django.db import models


class Person(models.Model):
    FIO_text = models.CharField(max_length=100)
    work_text = models.CharField(max_length=50)
    place_text = models.CharField(max_length=100, blank=True)
    marker_text = models.CharField(max_length=5, blank=True)


class History(models.Model):
    FIO_text = models.CharField(max_length=100)
    place_text = models.CharField(max_length=100)
    marker_text = models.CharField(max_length=5, blank=True)
    time_date = models.DateTimeField()
