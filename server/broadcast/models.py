from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class BroadcastMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    active = models.BooleanField(default=True)
    scheduled_for = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    active_until = models.DateTimeField(blank=True, null=True)

    @classmethod
    def activate_due_messages(cls, user=None):
        """
        Activate scheduled messages when their scheduled time has passed.
        The most recently scheduled due message becomes active per user.
        """
        now = timezone.now()
        # First, expire active messages whose duration ended.
        expiring = cls.objects.filter(active=True, active_until__isnull=False, active_until__lte=now)
        if user is not None:
            expiring = expiring.filter(user=user)
        expiring.update(active=False)

        due = cls.objects.filter(active=False, scheduled_for__isnull=False, scheduled_for__lte=now)
        if user is not None:
            due = due.filter(user=user)

        user_ids = due.values_list('user_id', flat=True).distinct()
        for user_id in user_ids:
            latest_due = (
                cls.objects
                .filter(user_id=user_id, active=False, scheduled_for__isnull=False, scheduled_for__lte=now)
                .order_by('-scheduled_for', '-id')
                .first()
            )
            if latest_due:
                cls.objects.filter(user_id=user_id, active=True).update(active=False)
                latest_due.activate_now()

    def _set_active_window(self):
        if self.duration_minutes:
            self.active_until = timezone.now() + timedelta(minutes=self.duration_minutes)
        else:
            # "Until I change" behavior
            self.active_until = None

    def activate_now(self):
        self.active = True
        self._set_active_window()
        self.save(update_fields=['active', 'active_until'])

    def save(self, *args, **kwargs):
        if self.active:
            BroadcastMessage.objects.filter(user=self.user, active=True).update(active=False)
            self._set_active_window()
        elif self.active_until is not None:
            self.active_until = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}: {self.message[:20]}'