from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Utilisateur(AbstractUser):
    user_id =models.CharField(primary_key=True,max_length=8)
    email=models.EmailField(unique=True)
    telephone=models.CharField(max_length=15,blank=True,null=True)
    role=models.CharField(max_length=20,choices=[('A','admin'),('B','user')],default='A')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



class Entreprise(models.Model):
    raison_social =models.CharField(max_length=200,blank=False,null=False)
    matricule_fiscale=models.CharField(max_length=17,unique=True)
    adresse=models.TextField()
    type_entreprise=models.CharField(max_length=200,choices=[('A','Batata'),('B','Bountou')],default='A')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    gerant =models.OneToOneField(Utilisateur,on_delete=models.CASCADE,related_name='entreprise')

    