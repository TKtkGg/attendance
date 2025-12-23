from django.db import models
from django.utils import timezone


class AttendanceStatus(models.TextChoices):
	CLOCK_IN = 'clock_in', '出勤'
	ABSENT = 'absent', '欠勤'
	BREAK_START = 'break_start', '休憩入り'
	BREAK_END = 'break_end', '休憩終わり'


class Employee(models.Model):
	full_name = models.CharField(max_length=100)
	employee_code = models.CharField(max_length=20, unique=True)
	department = models.CharField(max_length=80, blank=True)
	current_status = models.CharField(
		max_length=20,
		choices=AttendanceStatus.choices,
		default=AttendanceStatus.ABSENT,
	)
	last_action_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ['full_name']

	def __str__(self) -> str:
		return f"{self.full_name} ({self.employee_code})"


class AttendanceRecord(models.Model):
	employee = models.ForeignKey(
		Employee,
		on_delete=models.CASCADE,
		related_name='records',
	)
	status = models.CharField(max_length=20, choices=AttendanceStatus.choices)
	recorded_at = models.DateTimeField(default=timezone.now)
	note = models.CharField(max_length=255, blank=True)

	class Meta:
		ordering = ['-recorded_at']

	def __str__(self) -> str:
		action = self.get_status_display()
		return f"{self.employee.full_name} - {action} ({self.recorded_at:%Y/%m/%d %H:%M})"
