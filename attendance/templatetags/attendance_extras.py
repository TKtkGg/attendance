from django import template

from ..constants import STATUS_BADGES
from ..models import AttendanceStatus

register = template.Library()


@register.filter
def status_badge(value: str) -> str:
    """Return Bootstrap badge class for the given attendance status."""
    try:
        status = AttendanceStatus(value)
    except (ValueError, TypeError):
        return 'secondary'
    return STATUS_BADGES.get(status, 'secondary')
