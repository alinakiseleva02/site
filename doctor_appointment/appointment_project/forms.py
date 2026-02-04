from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    """Форма для записи на прием"""
    class Meta:
        model = Appointment
        fields = ['patient_name', 'patient_phone', 'patient_email', 'notes']
        widgets = {
            'patient_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше полное имя'
            }),
            'patient_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш номер телефона'
            }),
            'patient_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш email (необязательно)'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Дополнительная информация (симптомы, пожелания)',
                'rows': 3
            }),
        }
        labels = {
            'patient_name': 'Ваше имя',
            'patient_phone': 'Номер телефона',
            'patient_email': 'Email',
            'notes': 'Примечания',
        }