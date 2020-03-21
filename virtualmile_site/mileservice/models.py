from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Trinker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Pruegel(models.Model):
    schlaeger = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING,related_name='schlaeger')
    geschlagen = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING,related_name='geschlagen')
    created_date = models.DateTimeField(default=timezone.now)
#models.OneToOneField(User, on_delete=models.CASCADE)

class Kneipe(models.Model):
    name = models.TextField()
    trinker = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING)
    reihenfolge = models.IntegerField()

class Steuerung(models.Model):
    kneipe = models.ForeignKey(Kneipe, on_delete=models.DO_NOTHING)
    reactionrunden = models.IntegerField()


class Bier(models.Model):
    trinker = models.ForeignKey(Trinker, on_delete=models.CASCADE,related_name='biere')
    created_date = models.DateTimeField(default=timezone.now)

class ReactionChallenge(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    answered_at = models.DateTimeField()
    trinker = models.ForeignKey(Trinker, on_delete=models.CASCADE)

class QuestionTemplate(models.Model):
    questiontext = models.TextField()
    answertext = models.TextField()

class QuestionRound(models.Model):
    template = models.ForeignKey(QuestionTemplate, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

class QuestionAnswer(models.Model):
    trinker = models.ForeignKey(Trinker, on_delete=models.CASCADE)
    questionround = models.ForeignKey(QuestionRound, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

class Busfahrt(models.Model):
    created_date = models.DateTimeField(default=timezone.now)

class Bussitzer(models.Model):
    fahrt = models.ForeignKey(Busfahrt, on_delete=models.CASCADE)
    fahrer = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(default=timezone.now)
