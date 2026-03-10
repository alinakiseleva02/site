from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from django.urls import reverse
from .models import Specialization, Doctor, Schedule, Appointment
from .forms import AppointmentForm

def index(request):
    specializations = Specialization.objects.all()
    doctors = Doctor.objects.all()[:4]
    
    context = {
        'specializations': specializations,
        'doctors': doctors,
    }
    return render(request, 'index.html', context)

def specializations(request):
    specializations = Specialization.objects.all()
    
    context = {
        'specializations': specializations,
    }
    return render(request, 'specializations.html', context)

def doctors_by_specialization(request, specialization_id):
    specialization = get_object_or_404(Specialization, id=specialization_id)
    doctors = Doctor.objects.filter(specialization=specialization)
    
    context = {
        'specialization': specialization,
        'doctors': doctors,
    }
    return render(request, 'doctors.html', context)

def schedule(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    today = timezone.now().date()
    start_date = today + timedelta(days=1)
    end_date = start_date + timedelta(days=14)
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    schedules = Schedule.objects.filter(
        doctor=doctor,
        date__range=[start_date, end_date],
        is_available=True
    ).order_by('date', 'start_time')
    schedule_by_date = {}
    for schedule_item in schedules:
        date_str = schedule_item.date.strftime('%Y-%m-%d')
        if date_str not in schedule_by_date:
            schedule_by_date[date_str] = []
        schedule_by_date[date_str].append(schedule_item)
    
    context = {
        'doctor': doctor,
        'date_list': date_list,
        'schedule_by_date': schedule_by_date,
    }
    return render(request, 'schedule.html', context)

def book_appointment(request, schedule_id):
    schedule_item = get_object_or_404(Schedule, id=schedule_id, is_available=True)
    doctor = schedule_item.doctor
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.schedule = schedule_item
            appointment.save()
            schedule_item.is_available = False
            schedule_item.save()
            return redirect('appointment_confirmation', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    
    context = {
        'doctor': doctor,
        'schedule': schedule_item,
        'form': form,
    }
    return render(request, 'confirmation.html', context)

def appointment_confirmation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'appointment_confirmation.html', context)

def schedule(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    today = timezone.now().date()
    start_date = today + timedelta(days=1)
    end_date = start_date + timedelta(days=14)
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    schedules = Schedule.objects.filter(
        doctor=doctor,
        date__range=[start_date, end_date],
        is_available=True
    ).order_by('date', 'start_time')
    schedule_by_date = {}
    for schedule_item in schedules:
        date_str = schedule_item.date.strftime('%Y-%m-%d')
        if date_str not in schedule_by_date:
            schedule_by_date[date_str] = []
        schedule_by_date[date_str].append({
            'id': schedule_item.id,
            'start_time': schedule_item.start_time.strftime('%H:%M'),
            'end_time': schedule_item.end_time.strftime('%H:%M'),
            'book_url': reverse('book_appointment', args=[schedule_item.id])
        })
    
    context = {
        'doctor': doctor,
        'date_list': date_list,
        'schedule_by_date': schedule_by_date,
    }
    return render(request, 'schedule.html', context)