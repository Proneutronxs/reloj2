from django.db import models


# Create your models here.

class model_buscar_legajo(models.Model):
    legajo = models.IntegerField()
    departamento = models.CharField(max_length=25)
    desde = models.DateField()
    hasta = models.DateField()
