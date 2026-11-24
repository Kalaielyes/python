from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Vehicule(models.Model):
    immatricule = models.CharField(max_length=12, unique=True)
    capacite_kg = models.PositiveIntegerField(
        validators=[MinValueValidator(1, "Une capacité nulle ne peut pas être acceptée.")]
    )
    disponible = models.BooleanField(default=True)
    type_vehicule = models.CharField(
        max_length=20,
        choices=[
            ('camionnette', 'camionnette'),
            ('fourgon', 'fourgon'),
            ('camion_porteur', 'camion_porteur'),
            ('semi_remorque', 'semi_remorque')
        ],
        default='camionnette'
    )
    entreprise = models.ForeignKey(
        'EntrepriseApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='vehicules'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'transporteur':
            raise ValidationError({'entreprise': "L'entreprise doit être de type transporteur."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.immatricule} ({self.type_vehicule})"


