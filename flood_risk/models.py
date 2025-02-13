from django.db import models

# Create your models here.
class FloodRiskAssessment(models.Model):
    location = models.CharField(max_length=255)
    pipe_diameter = models.FloatField()
    last_inspection = models.DateField()
    damage_level = models.IntegerField()
    risk_score = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)