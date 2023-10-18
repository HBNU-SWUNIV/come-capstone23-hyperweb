from django.db import models

class Dog_Info(models.Model):
    dog_mer = models.FloatField(default=0)

    def __str__(self):
        return self.dog_mer
    
class Monthly_Food(models.Model):
    food_1 = models.ForeignKey(Dog_Info, related_name='food_items1', on_delete=models.CASCADE, null=True)
    food_2 = models.ForeignKey(Dog_Info, related_name='food_items2', on_delete=models.CASCADE, null=True)
    food_3 = models.ForeignKey(Dog_Info, related_name='food_items3', on_delete=models.CASCADE, null=True)
    food_4 = models.ForeignKey(Dog_Info, related_name='food_items4', on_delete=models.CASCADE, null=True)
    dog_info = models.ForeignKey(Dog_Info, related_name='food_month', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'{self.food_1} - {self.food_2} - {self.food_3} - {self.food_4} - {self.dog_info}'
    
class Food_Item(models.Model):
    name = models.CharField(max_length=100)
    unit = models.IntegerField()
    dog_info = models.ForeignKey(Dog_Info, related_name='food_items', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Food_Result(models.Model):
    name = models.CharField(max_length=100)
    unit = models.IntegerField()
    dog_info = models.ForeignKey(Dog_Info, related_name='food_result', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name} - {self.unit}"
    
class Nut_some_save(models.Model):
    dog_info = models.ForeignKey(Dog_Info, related_name='nut_some_save', on_delete=models.CASCADE, null=True)
    B10100 = models.FloatField()
    B10300 = models.FloatField()
    B10700 = models.FloatField()
    
    def __str__(self):
        return f"{self.dog_info} - {self.B10100} - {self.B10300} - {self.B10700}"
    

class Nut_7_save(models.Model):
    dog_info = models.ForeignKey(Dog_Info, related_name='nut_7_save', on_delete=models.CASCADE, null=True)
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
    dog_info = models.ForeignKey(Dog_Info, related_name='nut_sufficient_save', on_delete=models.CASCADE, null=True)
    token_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.dog_info} - {self.token_name}'
    
class Nut_report(models.Model):
    dog_info = models.ForeignKey(Dog_Info, related_name='nut_report', on_delete=models.CASCADE, null=True)
    nut_name = models.CharField(max_length=100)
    actual_num = models.FloatField()
    percent = models.FloatField()
    min_num = models.FloatField()
    
    def __str__(self):
        return f"{self.nut_name} - {self.actual_num} - {self.percent} - {self.min_num}"

class Get_Id(models.Model):
    dog_info_id = models.IntegerField()
    
    def __str__(self):
        return self.dog_info_id
    
# class Nut_save(models.Model):
#     nut_7_save = models.ForeignKey(Nut_7_save, related_name='nut_7_save', on_delete=models.CASCADE, null=True)
#     A10100 = models.FloatField()
#     A10200 = models.FloatField()
#     A10300 = models.FloatField()
#     A10400 = models.FloatField()
#     A10500 = models.FloatField()
#     A10600 = models.FloatField()
#     A10700 = models.FloatField()
#     A10800 = models.FloatField()
#     B10100 = models.FloatField()
#     B10200 = models.FloatField()
#     B10300 = models.FloatField()
#     B10400 = models.FloatField()
#     B10500 = models.FloatField()
#     B10600 = models.FloatField()
#     B10700 = models.FloatField()
#     B10800 = models.FloatField()
#     B10900 = models.FloatField()
#     B11000 = models.FloatField()
#     B11100 = models.FloatField()
#     B11200 = models.FloatField()
#     C10100 = models.FloatField()
#     C20100 = models.FloatField()
#     C20200 = models.FloatField()
#     C20300 = models.FloatField()
#     C20500 = models.FloatField()
#     C20600 = models.FloatField()
#     C20700 = models.FloatField()
#     C20900 = models.FloatField()
#     C21200 = models.FloatField()
#     C21300 = models.FloatField()
#     C10200 = models.FloatField()
#     C10300 = models.FloatField()
#     C10400 = models.FloatField()
#     D10100 = models.FloatField()
#     D10200 = models.FloatField()
#     E10100 = models.FloatField()
#     E10200 = models.FloatField()
#     E10400 = models.FloatField()
#     E10605 = models.FloatField()
#     E10700 = models.FloatField()
#     E10800 = models.FloatField()
#     E10900 = models.FloatField()
#     Z10300 = models.FloatField()

#     def __str__(self):
#         f"{self.nut_7_save}"
# # temp = ['A10100', 'A10200', 'A10300', 'A10400', 'A10500', 'A10600', 'A10700', 'A10701', 'A10702', 'A10703', 'A10704', 'A10705', 'A10706', 'A10800', 'A10801', 'A10802', 'B10100', 'B10200', 'B10300', 'B10400', 'B10500', 'B10600', 'B10700', 'B10800', 'B10900', 'B11000', 'B11100', 'B11200', 'C10100', 'C10102', 'C10103', 'C20100', 'C20200', 'C20300', 'C20301', 'C20302', 'C20303', 'C20500', 'C20600', 'C20601', 'C20700', 'C20900', 'C20901', 'C20902', 'C21200', 'C21300', 'C10200', 'C10201', 'C10202', 'C10300', 'C10301', 'C10302', 'C10303', 'C10304', 'C10305', 'C10306', 'C10307', 'C10308', 'C10400', 'C10401', 'C10402', 'D10100', 'D10200', 'D10201', 'D10202', 'D10203', 'D10204', 'D10205', 'D10206', 'D10207', 'D10208', 'D10209', 'D10210', 'D10301', 'D10302', 'D10303', 'D10304', 'D10305', 'D10306', 'D10307', 'D10308', 'D10309', 'E10100', 'E10200', 'E10300', 'E10400', 'E10401', 'E10402', 'E10403', 'E10404', 'E10405', 'E10406', 'E10407', 'E10408', 'E10409', 'E10410', 'E10411', 'E10412', 'E10413', 'E10414', 'E10415', 'E10416', 'E10615', 'E10500', 'E10502', 'E10503', 'E10504', 'E10505', 'E10506', 'E10507', 'E10508', 'E10509', 'E10600', 'E10601', 'E10602', 'E10603', 'E10605', 'E10606', 'E10607', 'E10609', 'E10610', 'E10611', 'E10612', 'E10614', 'E10700', 'E10800', 'E10900', 'E10901', 'E10902', 'E10903', 'Z10100', 'Z10300', 'Ratio1', 'Ratio2']
# # class Nut_save(models.Model):
    
# #     dog_info = models.ForeignKey(Dog_Info, related_name='food_items', on_delete=models.CASCADE, null=True)
# #     A10100 = models.IntegerField()
# #     A10200 = models.IntegerField()
# #     A10300 = models.IntegerField()
# #     A10400 = models.IntegerField()
# #     A10500 = models.IntegerField()
# #     A10600 = models.IntegerField()
# #     A10700 = models.IntegerField()
# #     A10701 = models.IntegerField()
# #     A10702 = models.IntegerField()
# #     A10703 = models.IntegerField()
# #     A10704 = models.IntegerField()
# #     A10705 = models.IntegerField()
# #     A10706 = models.IntegerField()
# #     A10800 = models.IntegerField()
# #     A10801 = models.IntegerField()
# #     A10802 = models.IntegerField()
# #     B10100 = models.IntegerField()
# #     B10200 = models.IntegerField()
# #     B10300 = models.IntegerField()
# #     B10400 = models.IntegerField()
# #     B10500 = models.IntegerField()
# #     B10600 = models.IntegerField()
# #     B10700 = models.IntegerField()
# #     B10800 = models.IntegerField()
# #     B10900 = models.IntegerField()
# #     B11000 = models.IntegerField()
# #     B11100 = models.IntegerField()
# #     B11200 = models.IntegerField()
# #     C10100 = models.IntegerField()
# #     C10102 = models.IntegerField()
# #     C10103 = models.IntegerField()
# #     C20100 = models.IntegerField()
# #     C20200 = models.IntegerField()
# #     C20300 = models.IntegerField()
# #     C20301 = models.IntegerField()
# #     C20302 = models.IntegerField()
# #     C20303 = models.IntegerField()
# #     C20500 = models.IntegerField()
# #     C20600 = models.IntegerField()
# #     C20601 = models.IntegerField()
# #     C20700 = models.IntegerField()
# #     C20900 = models.IntegerField()
# #     C20901 = models.IntegerField()
# #     C20902 = models.IntegerField()
# #     C21200 = models.IntegerField()
# #     C21300 = models.IntegerField()
# #     C10200 = models.IntegerField()
# #     C10201 = models.IntegerField()
# #     C10202 = models.IntegerField()
# #     C10300 = models.IntegerField()
# #     C10301 = models.IntegerField()
# #     C10302 = models.IntegerField()
# #     C10303 = models.IntegerField()
# #     C10304 = models.IntegerField()
# #     C10305 = models.IntegerField()
# #     C10306 = models.IntegerField()
# #     C10307 = models.IntegerField()
# #     C10308 = models.IntegerField()
# #     C10400 = models.IntegerField()
# #     C10401 = models.IntegerField()
# #     C10402 = models.IntegerField()
# #     D10100 = models.IntegerField()
# #     D10200 = models.IntegerField()
# #     D10201 = models.IntegerField()
# #     D10202 = models.IntegerField()
# #     D10203 = models.IntegerField()
# #     D10204 = models.IntegerField()
# #     D10205 = models.IntegerField()
# #     D10206 = models.IntegerField()
# #     D10207 = models.IntegerField()
# #     D10208 = models.IntegerField()
# #     D10209 = models.IntegerField()
# #     D10210 = models.IntegerField()
# #     D10301 = models.IntegerField()
# #     D10302 = models.IntegerField()
# #     D10303 = models.IntegerField()
# #     D10304 = models.IntegerField()
# #     D10305 = models.IntegerField()
# #     D10306 = models.IntegerField()
# #     D10307 = models.IntegerField()
# #     D10308 = models.IntegerField()
# #     D10309 = models.IntegerField()
# #     E10100 = models.IntegerField()
# #     E10200 = models.IntegerField()
# #     E10300 = models.IntegerField()
# #     E10400 = models.IntegerField()
# #     E10401 = models.IntegerField()
# #     E10402 = models.IntegerField()
# #     E10403 = models.IntegerField()
# #     E10404 = models.IntegerField()
# #     E10405 = models.IntegerField()
# #     E10406 = models.IntegerField()
# #     E10407 = models.IntegerField()
# #     E10408 = models.IntegerField()
# #     E10409 = models.IntegerField()
# #     E10410 = models.IntegerField()
# #     E10411 = models.IntegerField()
# #     E10412 = models.IntegerField()
# #     E10413 = models.IntegerField()
# #     E10414 = models.IntegerField()
# #     E10415 = models.IntegerField()
# #     E10416 = models.IntegerField()
# #     E10615 = models.IntegerField()
# #     E10500 = models.IntegerField()
# #     E10502 = models.IntegerField()
# #     E10503 = models.IntegerField()
# #     E10504 = models.IntegerField()
# #     E10505 = models.IntegerField()
# #     E10506 = models.IntegerField()
# #     E10507 = models.IntegerField()
# #     E10508 = models.IntegerField()
# #     E10509 = models.IntegerField()
# #     E10600 = models.IntegerField()
# #     E10601 = models.IntegerField()
# #     E10602 = models.IntegerField()
# #     E10603 = models.IntegerField()
# #     E10605 = models.IntegerField()
# #     E10606 = models.IntegerField()
# #     E10607 = models.IntegerField()
# #     E10609 = models.IntegerField()
# #     E10610 = models.IntegerField()
# #     E10611 = models.IntegerField()
# #     E10612 = models.IntegerField()
# #     E10614 = models.IntegerField()
# #     E10700 = models.IntegerField()
# #     E10800 = models.IntegerField()
# #     E10900 = models.IntegerField()
# #     E10901 = models.IntegerField()
# #     E10902 = models.IntegerField()
# #     E10903 = models.IntegerField()
# #     Z10100 = models.IntegerField()
# #     Z10300 = models.IntegerField()
# #     Ratio1 = models.IntegerField()
# #     Ratio2 = models.IntegerField()
# #     def __str__(self):
# #         return self.uid