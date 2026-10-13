from django.db import models
from django.utils import timezone
from EntrepriseApp.models import Entreprise
from django.core.exceptions import ValidationError


class Expedition(models.Model):
    STATUT_CHOICES = [
        ('publiee', 'Publiée'),
        ('attribuee', 'Attribuée'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    reference = models.CharField(max_length=20, unique=True, editable=False)

    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(max_digits=10, decimal_places=2)
    date_souhaitee = models.DateField()
    description = models.TextField(blank=True, null=True)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='publiee',
    )

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='expeditions',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.entreprise and self.entreprise.type_entreprise != 'c':
            raise ValidationError("L'entreprise associée doit être de type 'Chargeur'.")

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()
        super().save(*args, **kwargs)


    @classmethod
    def _generate_reference(cls):
        annee = timezone.now().strftime('%Y')
        prefix = f"EXP-{annee}-"

        dernier = cls.objects.filter(reference__startswith=prefix).order_by('reference').last()

        if dernier:
            try:
                num = int(dernier.reference.split('-')[-1]) + 1
            except (ValueError, IndexError):
                num = 1
        else:
            num = 1

        return f"{prefix}{num:05d}"


    def __str__(self):
        return f"{self.reference} ({self.ville_depart} → {self.ville_arrivee})"