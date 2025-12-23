from .models import AttendanceStatus

STATUS_BADGES = {
    AttendanceStatus.CLOCK_IN: 'success',
    AttendanceStatus.ABSENT: 'secondary',
    AttendanceStatus.BREAK_START: 'warning',
    AttendanceStatus.BREAK_END: 'info',
}
