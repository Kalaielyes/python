from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Vehicule(models.Model):
    TYPE_VEHICULE_CHOICES = [
        ('camionnette', 'Camionnette / utilitaire léger'),
        ('camion_porteur', 'Camion porteur'),
        ('semi_remorque', 'Semi-remorque'),
        ('fourgon', 'Fourgon'),
    ]

    immatriculation = models.CharField(max_length=20, unique=True)
    capacite_kg = models.PositiveIntegerField(
        validators=[MinValueValidator(1, "Une capacité nulle ne peut pas être acceptée.")]
    )
    disponible = models.BooleanField(default=True)
    type_vehicule = models.CharField(
        max_length=20,
        choices=TYPE_VEHICULE_CHOICES,
        default='camionnette'
    )
    entreprise = models.ForeignKey(
        'EntrepriseApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='vehicules'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Compatibility property for old code
    @property
    def immatricule(self):
        return self.immatriculation

    @immatricule.setter
    def immatricule(self, value):
        self.immatriculation = value

    def clean(self):
        super().clean()
        if self.capacite_kg is not None and self.capacite_kg <= 0:
            raise ValidationError({'capacite_kg': "Une capacité nulle ne peut pas être acceptée."})
        if self.entreprise_id and self.entreprise.type_entreprise != 'transporteur':
            raise ValidationError({'entreprise': "L'entreprise doit être de type transporteur."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.immatriculation} ({self.get_type_vehicule_display()})"
