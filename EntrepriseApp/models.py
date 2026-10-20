import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_gmail(value):
    if not value:
        raise ValidationError("L'adresse e-mail est obligatoire.")
    val = value.strip().lower()
    if not val.endswith('@gmail.com') or val.split('@')[-1] != 'gmail.com':
        raise ValidationError("Seuls les emails appartenant au domaine gmail.com sont acceptés.")


class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur'),
        ('admin', 'Admin'),
    ]

    user_id = models.CharField(max_length=8, primary_key=True, blank=True, editable=False)
    email = models.EmailField(unique=True, validators=[validate_gmail])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='chargeur')
    telephone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def _generate_user_id(cls):
        annee = timezone.now().strftime('%y')
        prefixe = f"{annee}user"
        dernier = cls.objects.filter(user_id__startswith=prefixe).order_by('user_id').last()
        compteur = (int(dernier.user_id[-2:]) + 1) if dernier else 0
        if compteur > 99:
            raise ValidationError("Limite de 99 utilisateurs atteinte pour cette année (00-99).")
        return f"{prefixe}{compteur:02d}"

    def clean(self):
        super().clean()
        if not self.user_id:
            self.user_id = self._generate_user_id()
        if self.email:
            validate_gmail(self.email)

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self._generate_user_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.user_id})"


matricule_fiscal_regex = r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPebdnp][/ -]?[MPCNEmpcne][/ -]?\d{3}$'
matricule_fiscal_validator = RegexValidator(
    regex=matricule_fiscal_regex,
    message="Format du Matricule Fiscal invalide (exemple: 1234567AAM000 ou 1234567/A/A/M/000 ou 1234567-A-A-M-000)."
)


class Entreprise(models.Model):
    TYPE_CHOICES = [
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur'),
    ]

    raison_sociale = models.CharField(max_length=200)
    matricule_fiscal = models.CharField(
        max_length=20,
        unique=True,
        validators=[matricule_fiscal_validator]
    )
    type_entreprise = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='chargeur'
    )
    adresse = models.TextField(
        validators=[MinLengthValidator(20, "L'adresse doit comporter au minimum 20 caractères.")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gerant = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')

    # Compatibility properties for old code or variations
    @property
    def raison_social(self):
        return self.raison_sociale

    @raison_social.setter
    def raison_social(self, value):
        self.raison_sociale = value

    @property
    def utilisateur(self):
        return self.gerant

    @utilisateur.setter
    def utilisateur(self, value):
        self.gerant = value

    def clean(self):
        super().clean()
        if self.adresse and len(self.adresse.strip()) < 20:
            raise ValidationError({'adresse': "L'adresse doit comporter au minimum 20 caractères."})
        if self.matricule_fiscal:
            if not re.match(matricule_fiscal_regex, self.matricule_fiscal):
                raise ValidationError({'matricule_fiscal': "Format du Matricule Fiscal invalide (exemple: 1234567AAM000 ou 1234567/A/A/M/000)."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.raison_sociale
