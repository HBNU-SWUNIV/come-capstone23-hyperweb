from make_report.models import Nutrient


nutrient1 = Nutrient(name='영양소1', minimum_value=10.0, actual_value=5.0)
nutrient1.save()

nutrient2 = Nutrient(name='영양소2', minimum_value=5.0, actual_value=1.5)
nutrient2.save()