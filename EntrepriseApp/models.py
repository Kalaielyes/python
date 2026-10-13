from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

# 1. VALIDATEURS (définis AVANT les classes)


matricule_fiscal_validator = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
    message="Format de matricule fiscal invalide. Exemple : 1234567A/B/M/123"
)

def validate_email(value):
    if not value:
        raise ValidationError("L'adresse e-mail est obligatoire.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValidationError("Format d'adresse e-mail invalide.")

    
adresse_validators = [
    MinLengthValidator(20, "L'adresse ne peut pas avoir moins de 20 caractères."),
    MaxLengthValidator(400, "L'adresse ne peut pas avoir plus de 400 caractères."),
]



# 2. MODÈLE Utilisateur


class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('c', 'Chargeur'),
        ('t', 'Transporteur'),
    ]

    user_id = models.CharField(primary_key=True, max_length=8)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='c')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.user_id:
            last = Utilisateur.objects.order_by('-user_id').first()
            next_num = 1
            if last and last.user_id.startswith('USR-'):
                try:
                    next_num = int(last.user_id.split('-')[1]) + 1
                except (IndexError, ValueError):
                    next_num = 1
            self.user_id = f"USR-{next_num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username



# 3. MODÈLE Entreprise 


class Entreprise(models.Model):
    TYPE_CHOICES = [
        ('c', 'Chargeur'),
        ('t', 'Transporteur'),
    ]

    raison_sociale = models.CharField(max_length=200)

    matricule_fiscal = models.CharField(
        max_length=25,
        unique=True,
        validators=[matricule_fiscal_validator],       # ← ✅ UTILISÉ
    )

    adresse = models.TextField(validators=adresse_validators)

    type_entreprise = models.CharField(max_length=1, choices=TYPE_CHOICES)

    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='entreprise',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.raison_sociale


