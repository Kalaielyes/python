from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.utils import timezone

# Create your models here.

class Expedition(models.Model):
    reference = models.CharField(primary_key = True, unique = True, editable = False, max_length=12,
                                 validators=[
                                    RegexValidator(
                                        regex=r'^EXP-\d{2}-\d{5}$',
                                        message='La référence doit suivre le format EXP-AA-NNNNN.'
                                    )
                                ])
    date_souhaitee = models.DateField()
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(decimal_places=3, max_digits=10, validators = [MinValueValidator(0.001, "le poids doit être < 0 kg")])
    description = models.TextField()
    statut = models.CharField(
        max_length=100,
        choices=[
            ('publiee', 'Publiée'),
            ('attribuee', 'Attribuée'),
            ('en_cours', 'En cours'),
            ('livree', 'Livrée'),
            ('annulee', 'Annulée'),
        ],
        default='publiee'
    )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    # foreign key to entreprise
    entreprise = models.ForeignKey(
        'EntrepriseApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='expeditions',
    )

    # vérifier qu'une entreprise est de type chargeur
    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':   #vérifier si l'entreprise existe
            raise ValidationError({
                'entreprise': 'Une expédition ne peut être céée que par une entreprise chargeur'
            })



    @classmethod
    def _generate_reference(cls):
        annee = timezone.now().strftime('%y')
        prefixe = f"EXP-{annee}-"

        dernier = (
            cls.objects.filter(reference__startswith=prefixe)
            .order_by('-reference')
            .first()
        )

        compteur = (
            int(dernier.reference[-5:]) + 1 if dernier else 1
        )

        if compteur > 99999:
            raise ValidationError("Limite de références atteinte.")

        return f"{prefixe}{compteur:05d}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()

        # Appliquer les validateurs avant l'enregistrement
        self.full_clean()
        super().save(*args, **kwargs)