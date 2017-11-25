# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BiometricData(models.Model):
    deviceUID = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def create(cls, user, deviceUID):
        biometric_data = cls(user=user, deviceUID=deviceUID)
        # do something with the book
        return biometric_data
