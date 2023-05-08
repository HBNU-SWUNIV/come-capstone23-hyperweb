from django.db import models

class Dog(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    ACTIVITY_CHOICES = [('L', 'Low'), ('M', 'Moderate'), ('H', 'High')]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    neutered = models.BooleanField()
    breed = models.CharField(max_length=100)
    weight = models.FloatField()
    weight_goal = models.CharField(max_length=10, choices=[('I', 'Increase'), ('D', 'Decrease'), ('M', 'Maintain')])
    activity_level = models.CharField(max_length=1, choices=ACTIVITY_CHOICES)

    improvement_area = models.CharField(max_length=200)
    allergies = models.CharField(max_length=200)
    medical_history = models.CharField(max_length=200)

    current_food_type = models.CharField(max_length=200)
    desired_feeding_frequency = models.IntegerField()

    ingredient_weight = models.FloatField()
    protein_ratio = models.FloatField()
    fat_ratio = models.FloatField()
    carbohydrate_ratio = models.FloatField()


# class jsonoutput(models.Model):

