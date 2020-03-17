from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Trinker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Trinker.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.trinker.save()

class Kneipe(models.Model):
    name = models.TextField()
    trinker = models.ForeignKey(Trinker, on_delete=models.DO_NOTHING)
    reihenfolge = models.IntegerField()

class Steuerung(models.Model):
    kneipe = models.ForeignKey(Kneipe, on_delete=models.DO_NOTHING)
    reactionrunden = models.IntegerField()


class Bier(models.Model):
    trinker = models.ForeignKey(Trinker, on_delete=models.CASCADE)
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
