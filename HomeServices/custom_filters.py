from django import template
from . models import User,ServiceRequest  # Replace with your actual profile model

register = template.Library()

@register.filter(name='get_profile')
def get_profile(user_id):
    try:
        profile = User.objects.get(username=user_id)
        return profile
    except User.DoesNotExist:
        return None
