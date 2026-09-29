from django.db import models
from VehiculeApp.models import Vehicule
from ExpeditionApp.models import Expedition
from EntrepriseApp.models import Entreprise
# Create your models here.
class Offre(models.Model):
    delai_jour=models.IntegerField()
    prix=models.FloatField()
    date_proposition=models.DateTimeField(auto_now_add=True)
    statut =models.CharField(choices=[('A','online'),('B','offline')],default='A')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    vehicule=models.ForeignKey(Vehicule,on_delete=models.CASCADE,related_name='offres')
    expedition=models.ForeignKey(Expedition,on_delete=models.CASCADE,related_name='offres')
    entreprise=models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='offres')
    
