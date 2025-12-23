from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, render

from .constants import STATUS_BADGES
from .forms import AttendanceActionForm
from .models import AttendanceRecord, AttendanceStatus, Employee


def attendance_panel(request):
	form = AttendanceActionForm(request.POST or None)
	recent_records = AttendanceRecord.objects.select_related('employee')[:8]

	if request.method == 'POST':
		form = AttendanceActionForm(request.POST)
		if form.is_valid():
			employee = form.cleaned_data['employee']
			status_value = form.cleaned_data['status']
			note = form.cleaned_data['note']

			record = AttendanceRecord.objects.create(
				employee=employee,
				status=status_value,
				note=note,
			)

			employee.current_status = status_value
			employee.last_action_at = record.recorded_at
			employee.save(update_fields=['current_status', 'last_action_at'])

			status_label = AttendanceStatus(status_value).label
			messages.success(
				request,
				f"{employee.full_name} さんを「{status_label}」として記録しました。",
			)
			return redirect('attendance:panel')

		messages.error(request, '入力内容を確認してください。')

	context = {
		'form': form,
		'recent_records': recent_records,
	}
	return render(request, 'attendance/panel.html', context)


def status_dashboard(request):
	employees = Employee.objects.all()
	status_counts = {status.value: 0 for status in AttendanceStatus}
	aggregated = (
		Employee.objects.values('current_status')
		.order_by()
		.annotate(total=Count('id'))
	)

	for row in aggregated:
		key = row['current_status']
		if key in status_counts:
			status_counts[key] = row['total']

	status_summary = [
		{
			'value': status.value,
			'label': status.label,
			'count': status_counts[status.value],
		}
		for status in AttendanceStatus
	]

	context = {
		'employees': employees,
		'status_summary': status_summary,
	}
	return render(request, 'attendance/dashboard.html', context)
