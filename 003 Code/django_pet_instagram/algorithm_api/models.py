from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class FoodList(models.Model):
    foods = models.ManyToManyField(Food)

    def __str__(self):
        return ", ".join([str(food) for food in self.foods.all()])
