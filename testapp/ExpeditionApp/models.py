from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone


class Expedition(models.Model):
    reference = models.CharField(max_length=50, unique=True, editable=False)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.PositiveIntegerField(
        validators=[MinValueValidator(1, "Ne pas accepter un poids nul.")]
    )
    date_souhaitee = models.DateField()
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('publiee', 'Publiée'),
            ('attribuee', 'Attribuée'),
            ('en_cours', 'En cours'),
            ('livree', 'Livrée'),
            ('annulee', 'Annulée'),
        ],
        default='publiee',
    )
    entreprise = models.ForeignKey(
        'EntrepriseApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='expeditions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError({'entreprise': "Une expédition ne peut être créée que par une entreprise de type chargeur."})

    @classmethod
    def _generate_ref(cls):
        annee = timezone.now().strftime('%y')
        prefixe = f"EXP-{annee}-"
        dernier = cls.objects.filter(reference__startswith=prefixe).order_by('reference').last()
        compteur = (int(dernier.reference.split('-')[-1]) + 1) if dernier else 1
        if compteur > 99999:
            raise ValidationError("Limite de 99999 expéditions atteinte pour cette année.")
        return f"{prefixe}{compteur:05d}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_ref()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} ({self.statut})"

        
        
   