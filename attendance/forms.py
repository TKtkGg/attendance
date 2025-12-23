from django import forms

from .models import AttendanceStatus, Employee


class AttendanceActionForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.none(),
        label='従業員',
        empty_label='従業員を選択してください',
    )
    note = forms.CharField(
        label='メモ (任意)',
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': '打刻に関する補足があれば入力'}),
    )
    status = forms.ChoiceField(
        choices=AttendanceStatus.choices,
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employee.objects.order_by('full_name')
        self.fields['status'].initial = AttendanceStatus.CLOCK_IN
        self.fields['employee'].widget.attrs.update({'class': 'form-select'})
        self.fields['note'].widget.attrs.update({'class': 'form-control'})
