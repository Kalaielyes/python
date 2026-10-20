from decimal import Decimal
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone


class Offre(models.Model):
    STATUT_CHOICES = [
        ('proposee', 'Proposée'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
    ]

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'), "Le prix doit être strictement supérieur à 0.")]
    )
    delai_jours = models.PositiveIntegerField(
        validators=[MinValueValidator(1, "Le délai doit être supérieur ou égal à 1 jour.")]
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='proposee',
    )
    date_proposition = models.DateField(default=timezone.now)

    expedition = models.ForeignKey(
        'ExpeditionApp.Expedition',
        on_delete=models.CASCADE,
        related_name='offres',
    )
    transporteur = models.ForeignKey(
        'EntrepriseApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='offres_proposees',
    )
    vehicule = models.ForeignKey(
        'VehiculeApp.Vehicule',
        on_delete=models.CASCADE,
        related_name='offres',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['expedition', 'transporteur'],
                condition=models.Q(statut='proposee'),
                name='unique_offre_proposee_par_transporteur'
            )
        ]

    def clean(self):
        super().clean()

        if self.prix is not None and self.prix <= Decimal('0'):
            raise ValidationError({'prix': "Le prix doit être strictement supérieur à 0."})

        if self.delai_jours is not None and self.delai_jours < 1:
            raise ValidationError({'delai_jours': "Le délai doit être supérieur ou égal à 1 jour."})

        # Règle 1 : Une offre ne peut être créée que par une entreprise dont type_entreprise = transporteur
        if self.transporteur_id and self.transporteur.type_entreprise != 'transporteur':
            raise ValidationError({
                'transporteur': "Une offre ne peut être créée que par une entreprise dont type_entreprise = transporteur."
            })

        # Règle 2 : Le véhicule associé à une offre doit appartenir à la même entreprise que le transporteur de l'offre
        if self.vehicule_id and self.transporteur_id and self.vehicule.entreprise_id != self.transporteur_id:
            raise ValidationError({
                'vehicule': "Le véhicule associé à une offre doit appartenir à la même entreprise que le transporteur de l'offre."
            })

        is_new = self._state.adding or not self.pk

        # Règle 3 : Une expédition ne peut recevoir de nouvelles offres que si son statut est 'publiee'
        if is_new and self.expedition_id and self.expedition.statut != 'publiee':
            raise ValidationError({
                'expedition': "Une expédition ne peut recevoir de nouvelles offres que si son statut est 'publiee'."
            })

        # Règle 4 : Une entreprise ne peut pas avoir deux offres au statut 'proposee' actives simultanément sur la même expédition
        if self.statut == 'proposee' and self.transporteur_id and self.expedition_id:
            doublon = Offre.objects.filter(
                expedition_id=self.expedition_id,
                transporteur_id=self.transporteur_id,
                statut='proposee'
            )
            if self.pk:
                doublon = doublon.exclude(pk=self.pk)
            if doublon.exists():
                raise ValidationError(
                    "Une entreprise ne peut pas avoir deux offres au statut 'proposée' actives simultanément sur la même expédition."
                )

        # Règle 6 : Un véhicule dont disponible = False ne peut pas être proposé sur une nouvelle offre
        if is_new and self.vehicule_id and not self.vehicule.disponible:
            raise ValidationError({
                'vehicule': "Un véhicule dont disponible = False ne peut pas être proposé sur une nouvelle offre."
            })

        # Règle 7 : L'attribut type_vehicule conditionne la compatibilité avec le poids d'une expédition
        if self.vehicule_id and self.expedition_id:
            CAPACITE_MAX = {
                'camionnette': 1500,        # Jusqu'à ~1,5 t
                'fourgon': 3500,            # ~3,5 t
                'camion_porteur': 19000,    # ~3,5 à 19 t
                'semi_remorque': 26000,     # ~19 à 26 t
            }
            poids = self.expedition.poids_kg
            if self.vehicule.capacite_kg and poids > self.vehicule.capacite_kg:
                raise ValidationError({
                    'vehicule': f"Le poids de l'expédition ({poids} kg) dépasse la capacité réelle du véhicule ({self.vehicule.capacite_kg} kg)."
                })
            capacite_type = CAPACITE_MAX.get(self.vehicule.type_vehicule)
            if capacite_type is not None and poids > capacite_type:
                raise ValidationError({
                    'vehicule': (
                        f"Le véhicule de type '{self.vehicule.get_type_vehicule_display()}' "
                        f"ne peut pas transporter {poids} kg (capacité indicative maximale : {capacite_type} kg)."
                    )
                })

    @transaction.atomic
    def save(self, *args, **kwargs):
        statut_precedent = None
        if self.pk:
            try:
                statut_precedent = Offre.objects.get(pk=self.pk).statut
            except Offre.DoesNotExist:
                pass

        self.full_clean()
        super().save(*args, **kwargs)

        # Règle 5 : Cascade à l'acceptation
        # Quand une offre passe au statut « acceptee », l'expédition associée passe automatiquement à « attribuee »,
        # et toutes les autres offres « proposee » sur cette même expédition passent automatiquement à « refusee ».
        if self.statut == 'acceptee' and statut_precedent != 'acceptee':
            Expedition = self.expedition.__class__
            Expedition.objects.filter(pk=self.expedition_id).update(statut='attribuee')
            self.expedition.statut = 'attribuee'

            Offre.objects.filter(
                expedition_id=self.expedition_id,
                statut='proposee'
            ).exclude(pk=self.pk).update(statut='refusee')

    def __str__(self):
        return f"Offre {self.id} ({self.prix} DT) - {self.get_statut_display()}"
