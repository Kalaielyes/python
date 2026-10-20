from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone

ref_validator = RegexValidator(
    regex=r'^EXP-\d{2}-\d{5}$',
    message="La référence doit être au format EXP-AA-NNNNN."
)


class Expedition(models.Model):
    STATUT_CHOICES = [
        ('publiee', 'Publiée'),
        ('attribuee', 'Attribuée'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    reference = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        editable=False,
        validators=[ref_validator]
    )
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'), "Ne pas accepter un poids nul.")]
    )
    date_souhaitee = models.DateField()
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='publiee',
    )
    entreprise = models.ForeignKey(
        'EntrepriseApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='expeditions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Compatibility property for old code
    @property
    def ville_arrive(self):
        return self.ville_arrivee

    @ville_arrive.setter
    def ville_arrive(self, value):
        self.ville_arrivee = value

    @classmethod
    def _generate_ref(cls):
        annee = timezone.now().strftime('%y')
        prefixe = f"EXP-{annee}-"
        dernier = cls.objects.filter(reference__startswith=prefixe).order_by('reference').last()
        compteur = (int(dernier.reference.split('-')[-1]) + 1) if dernier else 1
        if compteur > 99999:
            raise ValidationError("Limite de 99999 expéditions atteinte pour cette année.")
        return f"{prefixe}{compteur:05d}"

    def clean(self):
        super().clean()
        if not self.reference:
            self.reference = self._generate_ref()
        if self.poids_kg is not None and self.poids_kg <= Decimal('0'):
            raise ValidationError({'poids_kg': "Ne pas accepter un poids nul."})
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError({'entreprise': "Une expédition ne peut être créée que par une entreprise de type chargeur."})

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_ref()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} ({self.get_statut_display()})"
