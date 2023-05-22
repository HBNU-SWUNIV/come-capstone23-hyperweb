from django.db import models

class Nutrient(models.Model):
    name = models.CharField(max_length=100)
    minimum_value = models.DecimalField(max_digits=6, decimal_places=2)
    actual_value = models.DecimalField(max_digits=6, decimal_places=2)


def add_nutrient_data():
    nutrient1 = Nutrient(name='영양소1', minimum_value=10.0, actual_value=5.0)
    nutrient1.save()

    nutrient2 = Nutrient(name='영양소2', minimum_value=5.0, actual_value=1.5)
    nutrient2.save()

    nutrient3 = Nutrient(name='영양소3', minimum_value=10.0, actual_value=15.0)
    nutrient3.save()

    nutrient4 = Nutrient(name='영양소4', minimum_value=5.0, actual_value=21.5)
    nutrient4.save()
