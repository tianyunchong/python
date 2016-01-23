# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class BugAnaly(models.Model):
    urlid = models.IntegerField()
    url = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    status = models.IntegerField()
    uptime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bug_analy'


class BugUrls(models.Model):
    url = models.CharField(max_length=100)
    updatetime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bug_urls'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
