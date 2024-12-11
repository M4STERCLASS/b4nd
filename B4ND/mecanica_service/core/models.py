from django.db import models
from django.contrib.auth.models import User

#perfil del mecánico, extendiendo la información básica del usuario
class MechanicProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience_years = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username #retorna el nombre de usuario asociado al perfil de mecánico

#info. sobre los servicios ofrecidos por los mecánicos
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('MANT', 'Mantenimiento'),
        ('REPA', 'Reparación'),
        ('OTRO', 'Otro')
    ]

    mechanic = models.ForeignKey(MechanicProfile, on_delete=models.CASCADE, related_name='services') #cada servicio pertenece a un mecánico, en caso de que se elimine uno, se eliminan sus servicios
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, default='OTRO')
    details = models.TextField(default="") 
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.mechanic.user.username}" #muestra el nombre del servicio y el nombre de usuario del mecánico que lo ofrece

#bookings de los usuarios sobre los servicios específicos
class Booking(models.Model):
    STATUS_CHOICES = [
        ('PEND', 'Pendiente'),
        ('CONF', 'Confirmada'),
        ('COMP', 'Completada'),
        ('CANC', 'Cancelada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings') #usuario que realiza la reserva, al igual que 'mechanic', si se elimina 'user' se eliminan sus reservas
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings') #mismo procedimiento de 'user' y 'mechanic' aquí
    date = models.DateField()
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='PEND') #booking status

    def __str__(self):
        return f"Booking {self.id} - {self.service.name} ({self.get_status_display()})"

#MODELO PREVISTO, NO ESTÁ IMPLEMENTADO
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    payment_data = models.JSONField(default=dict)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"Payment for booking {self.booking.id}"
