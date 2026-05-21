from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        from users.tasks import send_email
        send_email.delay(
            "Welcome to Goodreads",
            f"Hi {instance.username}! Welcome to Goodreads",
            [instance.email],
        )