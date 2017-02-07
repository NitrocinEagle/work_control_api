from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class TimeControl(models.Model):
    user = models.ForeignKey(User, verbose_name='Сотрудник', related_name='time_controls')
    start = models.DateTimeField('Старт', auto_now_add=True, null=True, blank=True)
    end = models.DateTimeField('Стоп', null=True, blank=True)
    comment = models.TextField('Комменарии', null=True, blank=True)

    def __str__(self):
        start = self.start.strftime('%H:%M:%S -')
        end = self.end.strftime('%H:%M:%S  (%d.%m.%y)') if self.end else ""
        return "{}. {} {}".format(self.user, start, end)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
