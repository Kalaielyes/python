from django.db import models

# Create your models here.
class Expedition(models.Model):
    reference=models.CharField(max_length=200,unique=True)
    ville_depart=models.CharField(max_length=200,blank=False,unique=True)
    ville_arrive=models.CharField(max_length=200,blank=False,unique=True)
    poids_kg=models.FloatField()
    date_souhaitee=models.DateTimeField(auto_now_add=True)
    description=models.CharField(max_length=200)
    statut =models.CharField(choices=[('A','online'),('B','offline')],default='A')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

       
    