from django.contrib import admin
from .models import Specialization, Doctor, Schedule, Appointment

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'specialization', 'experience')
    list_filter = ('specialization',)
    search_fields = ('last_name', 'first_name')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time', 'is_available')
    list_filter = ('doctor', 'date', 'is_available')
    search_fields = ('doctor__last_name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor', 'schedule', 'created_at', 'is_confirmed')
    list_filter = ('doctor', 'created_at', 'is_confirmed')
    search_fields = ('patient_name', 'patient_phone')
    readonly_fields = ('created_at',)