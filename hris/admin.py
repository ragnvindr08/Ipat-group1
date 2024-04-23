from django.contrib import admin

# Register your models here.
from .models import *
from datetime import datetime

class AttendanceRecordAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the admin panel
    list_display = ('employee_id', 'date', 'time_in','break_in','break_out', 'time_out', 'surplusHour_time_in', 'surplusHour_time_out')

    def get_queryset(self, request):
        # Override get_queryset method to apply custom ordering
        return super().get_queryset(request).order_by('employee_id', 'date')

class OfficialTimeAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the admin panel
    list_display = ('employee_id', 'day', 'semester_id', 'official_office_in', 'official_office_out', 'official_honorarium_time_in', 'official_honorarium_time_out', 'official_servicecredit_time_in', 'official_servicecredit_time_out', 'official_overtime_time_in', 'official_overtime_time_out')

    def get_queryset(self, request):
        # Override get_queryset method to apply custom ordering
        return super().get_queryset(request).order_by('employee_id', 'day')


admin.site.register(Employee)
admin.site.register(OfficialTime,OfficialTimeAdmin)
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)
admin.site.register(EditLogs)