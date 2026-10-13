from django.db import models
from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule
from ExpeditionApp.models import Expedition
from django.core.exceptions import ValidationError


class Offre(models.Model):
    STATUT_CHOICES = [
        ('proposee', 'Proposée'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('retiree', 'Retirée'),
    ]

    prix = models.DecimalField(max_digits=10, decimal_places=2)


    delai_jours = models.PositiveIntegerField()

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='proposee',
    )


    date_proposition = models.DateField(auto_now_add=True)

    expedition = models.ForeignKey(
        Expedition,
        on_delete=models.CASCADE,
        related_name='offres',
    )

    transporteur = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='offres_proposees',
    )


    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='offres',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offre {self.prix} € / {self.delai_jours}j — {self.get_statut_display()}"

    

    def clean(self):
        super().clean()
        if  self and self.transporteur.type_entreprise != 't':
            raise ValidationError("L'entreprise associée doit être de type 'Transporteur'.")
        if  self.vehicule and self.vehicule.entreprise != self.transporteur:
            raise ValidationError("Le véhicule doit appartenir au transporteur associé à l'offre.")
        if  self.expedition and self.expedition.entreprise.type_entreprise != 'c':
            raise ValidationError("L'entreprise associée à l'expédition doit être de type 'Chargeur'.")
        if offre := Offre.objects.filter(expedition=self.expedition, transporteur=self.transporteur).exclude(pk=self.pk).first():
            raise ValidationError("Une offre pour cette expédition par ce transporteur existe déjà.")
        
        self.full_clean()  # Valide le modèle avant de le sauvegarder

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.statut == 'acceptee':
            # Mettre à jour le statut de l'expédition associée
            self.expedition.statut = 'attribuee'
            self

            offre = Offre.objects.filter(expedition=self.expedition).exclude(pk=self.pk)
            for offre in offre:
                offre.statut = 'refusee'
                offre.save()

    