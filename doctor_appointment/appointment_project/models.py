from django.db import models
from django.utils import timezone

class Specialization(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название специализации")
    description = models.TextField(verbose_name="Описание", blank=True)
    icon = models.CharField(max_length=50, default="fas fa-user-md", verbose_name="Иконка")
    
    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, verbose_name="Специализация")
    experience = models.IntegerField(verbose_name="Стаж (лет)")
    description = models.TextField(verbose_name="Описание", blank=True)
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True, verbose_name="Фотография")
    
    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.specialization.name}"

class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Врач")
    date = models.DateField(verbose_name="Дата приема")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    is_available = models.BooleanField(default=True, verbose_name="Доступно для записи")
    
    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time}-{self.end_time}"

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100, verbose_name="Имя пациента")
    patient_phone = models.CharField(max_length=20, verbose_name="Телефон пациента")
    patient_email = models.EmailField(verbose_name="Email пациента", blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Врач")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name="Расписание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    notes = models.TextField(verbose_name="Примечания", blank=True)
    is_confirmed = models.BooleanField(default=False, verbose_name="Подтверждено")
    
    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.patient_name} - {self.doctor} - {self.schedule.date}"