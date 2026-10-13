from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from EntrepriseApp.models import Entreprise
from django.core.exceptions import ValidationError


class Vehicule(models.Model):
    TYPE_CHOICES = [
        ('camionnette', 'Camionnette'),
        ('fourgon', 'Fourgon'),
        ('camion_porteur', 'Camion porteur'),
        ('semi_remorque', 'Semi-remorque'),
    ]

    immatriculation = models.CharField(max_length=20, unique=True)
    type_vehicule = models.CharField(max_length=20, choices=TYPE_CHOICES)

    capacite_kg = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, "La capacité doit être supérieure à 0 kg"),
            MaxValueValidator(10000, "La capacité ne peut pas dépasser 10000 kg"),
        ]
    )

    disponible = models.BooleanField(default=True)

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='vehicules',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.immatriculation} ({self.get_type_vehicule_display()})"

    def clean(self):
        super().clean()
        if self.entreprise and self.entreprise.type_entreprise != 't':
            raise ValidationError("L'entreprise associée doit être de type 'Transporteur'.")

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)