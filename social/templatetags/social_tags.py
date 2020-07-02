from django import template
from django.utils import timezone
register = template.Library()

@register.filter
def daysCount(published_date):
    current_date = timezone.now()
    return (current_date - published_date).days
