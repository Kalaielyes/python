from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_email(value):
    if not value:
        raise ValidationError('adresse e-mail obligatoire')
    if not value.endswith('@gmail.com'):
        raise ValidationError('domaine accepté est gmail')


matricule_fiscale_validator = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
    message='format erroné'
)


class Utilisateur(AbstractUser):
    # PK personnalisée : AAuserNN (ex. 26user00)
    user_id = models.CharField(primary_key=True, max_length=8, editable=False)
    email = models.EmailField(unique=True, validators=[validate_email])
    telephone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('c', 'Chargeur'),
        ('t', 'Transporteur'),
    ], default='c')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def _generate_user_id(cls, year):
        prefix = f"{year % 100:02d}user"          # AA + "user"
        last = (cls.objects
                .select_for_update()
                .filter(user_id__startswith=prefix)
                .order_by('-user_id')
                .first())
        n = int(last.user_id[-2:]) + 1 if last else 0   # NN : 00 si 1er de l'année
        if n > 99:
            raise ValidationError(f"Limite de 100 utilisateurs atteinte pour l'année {year}.")
        return f"{prefix}{n:02d}"

    def save(self, *args, **kwargs):
        if not self.user_id:
            with transaction.atomic():
                year = (self.date_joined or timezone.now()).year
                self.user_id = self._generate_user_id(year)
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


class Entreprise(models.Model):
    raison_social = models.CharField(max_length=200, blank=False, null=False)
    matricule_fiscale = models.CharField(max_length=17, unique=True,
                                         validators=[matricule_fiscale_validator])
    adresse = models.TextField(validators=[
        MinLengthValidator(20, "L'adresse doit avoir au moins 20 caractères"),
        MaxLengthValidator(400, "L'adresse ne peut pas dépasser 400 caractères")
    ])
    type_entreprise = models.CharField(max_length=100, choices=[
        ('c', 'Chargeur'),
        ('t', 'Transporteur')
    ], default='c')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gerant = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='entreprise')