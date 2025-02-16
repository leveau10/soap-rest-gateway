from django.db import models

class Time(models.Model):
    nome = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    
