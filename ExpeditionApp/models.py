from django.db import models
from EntrepriseApp.models import Entreprise
from django.utils import timezone
from django.core.validators import MinValueValidator


class Expedition(models.Model):
    reference = models.CharField(max_length=50, unique=True)
    ville_depart = models.CharField(max_length=80)
    ville_arrive = models.CharField(max_length=80)

    poids_kg = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[
            MinValueValidator(0.001, "Le poids doit être supérieur à 0 kg"),
        ]
    )

    date_souhaitee = models.DateTimeField()
    description = models.TextField()

    statut = models.CharField(
        max_length=100,
        choices=[
            ('en_attente', 'en_attente'),
            ('t', 'terminee'),
            ('a', 'annulee')
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='entreprise'
    )

    @classmethod
    def _generate_reference(cls):
        annee = timezone.now().strftime('%Y')
        prefix = f"EXP-{annee}-"

        dernier = (
            cls.objects
            .filter(reference__startswith=prefix)
            .order_by('reference')
            .last()
        )

        compteur = (
            int(dernier.reference[-5:]) + 1
            if dernier
            else 1
        )

        if compteur > 99999:
            raise ValueError("Limite dépassée")

        return f"{prefix}{compteur:05d}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()

        self.full_clean()

        super().save(*args, **kwargs)
