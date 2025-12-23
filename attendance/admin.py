from django.contrib import admin

from .models import AttendanceRecord, Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'employee_code', 'department', 'current_status', 'last_action_at')
	list_filter = ('department', 'current_status')
	search_fields = ('full_name', 'employee_code', 'department')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
	list_display = ('employee', 'status', 'recorded_at', 'note')
	list_filter = ('status', 'recorded_at')
	search_fields = ('employee__full_name', 'employee__employee_code', 'note')
