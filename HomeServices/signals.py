# homeservices/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, **kwargs):
    if instance.is_active and kwargs.get('update_fields') == {'is_active'}:
        subject = 'Your account has been activated'
        message = 'Welcome to HomeCareServices! Your account has been activated by the admin.'
        from_email = 'missionimpossible4546@gmail.com'  # Replace with your admin's email address
        recipient_list = ['ganeshyarrampati999@gmail.com']
        print("                       send_mail ")

        send_mail(subject, message, from_email, recipient_list)
