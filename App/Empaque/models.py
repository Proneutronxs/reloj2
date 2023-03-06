from django.db import models

# Create your models here.

class model_buscar_reportes_camaras(models.Model):
    fechaReporte = models.DateField()
    hora = models.CharField(max_length=25, null=True)
    planta = models.CharField(max_length=25)

