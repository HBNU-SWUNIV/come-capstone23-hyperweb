from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Monthly_Food(models.Model):
    food_1 = models.IntegerField()
    food_2 = models.IntegerField()
    food_3 = models.IntegerField()
    food_4 = models.IntegerField()
    month_id = models.IntegerField()
    
    def __str__(self):
        return f'{self.food_1} - {self.food_2} - {self.food_3} - {self.food_4}'
        
class Food_Item(models.Model):
    name = models.CharField(max_length=100)
    unit = models.IntegerField()
    dog_info = models.IntegerField()

    def __str__(self):
        return self.name
    
class Nut_7_save(models.Model):
    dog_info = models.IntegerField()
    A10100 = models.FloatField()
    A10300 = models.FloatField()
    A10400 = models.FloatField()
    A10600 = models.FloatField()
    A10700 = models.FloatField()
    suffient = models.IntegerField()
    lack = models.IntegerField()
    
    def __str__(self):
        return f"{self.dog_info} - {self.A10100} - {self.A10300} - {self.A10400} - {self.A10600} - {self.A10700} - {self.suffient} - {self.lack}"
    
class Nut_sufficient(models.Model):
    dog_info = models.IntegerField()
    token_name = models.CharField(max_length=7)
    
    def __str__(self):
        return f'{self.token_name}'

class Nut_report(models.Model):
    dog_info = models.IntegerField()
    nut_name = models.CharField(max_length=100)
    actual_num = models.FloatField()
    percent = models.IntegerField()
    min_num = models.FloatField()
    
    def __str__(self):
        return f"{self.nut_name} - {self.actual_num} - {self.percent} - {self.min_num}"
