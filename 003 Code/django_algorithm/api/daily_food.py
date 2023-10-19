import math
from itertools import zip_longest

from ortools.linear_solver import pywraplp

from .database import FoodSearch

class DietOptimizer:
    # RANGES = [(0, 7), (13, 14), (16, 29), (31, 34), (37, 39), (40, 42), (44, 47), (49, 50),
    #             (60, 61), (61, 63), (82, 84), (85, 86), (102, 103), (123, 127), (131, 132)]
    
    def __init__(self, dog_mer, input_data, db_file):
        self.dog_mer = dog_mer
        self.input_data = input_data
        
        self.searching_food = FoodSearch()
        self.searching_food.connect_db(db_file)
        self.user_food_nut_all = self.searching_food.get_input_list(input_data)
        self.user_food_nut_range = self.searching_food.get_calcurate_list(input_data)
        self.searching_food.close_db()
        # Instantiate a Glop solver and naming it.
        self.solver = pywraplp.Solver.CreateSolver('GLOP')
        if not self.solver:
            print('self.solver 오류')
        self.aim_nut_list = []
        
        self.foods = []
        self.nut_some = []
        self.calculated_recipe = []
        self.result_list = [0 for _ in range(132)]

            
    def solver_gen(self):
        self.solver = pywraplp.Solver.CreateSolver('GLOP')
        if not self.solver:
            print('solver 오류')
            
    def solver_check(self):
        status = self.solver.Solve()
        print('status :',status)
        # Check that the problem has an optimal solution.
        if status != self.solver.OPTIMAL:
            print('The problem does not have an optimal solution!')
            if status == self.solver.FEASIBLE:
                print('A potentially suboptimal solution was found.')
            elif status == self.solver.INFEASIBLE:
                print('The self.solver determined the problem to be infeasible.')
            elif status == self.solver.UNBOUNDED:
                print('The problem is unbounded.')
            elif status == self.solver.ABNORMAL:
                print('The self.solver encountered an abnormal condition.')
            elif status == self.solver.NOT_SOLVED:
                print('The self.solver could not solve the problem.')
            elif status == self.solver.MODEL_INVALID:
                print('The model is invalid.')
            elif status == self.solver.OUT_OF_MEMORY:
                print('The self.solver ran out of memory.')
            return False
        else:
            return True
        
    def calories_cal(self):
        print('calories_cal')
        select_list = ['A10100','A10300','A10400','A10600','D10201','D10202','D10203','D10204','D10205','D10206','D10207','D10208','D10209','D10210']
        
        adult_nutrient_max_list = [0.0] * 14
        # 아래의 기준은 1000kcal 기준 -> dog_mer에 따라 변동되야함  // 영양소 최대값도 동일 
        # ex) dog mer이 500kcal 일시 모든 기준에 나누기 2
        adult_nutrient_min_list = [0.0, 0.0, 0.0, 0.0, 950., 1700., 1580., 830., 1130., 1200., 400., 1230., 480., 1280.]
        # coefficient = self.dog_mer / 1000
        # fixed_nutrient_list = [value * coefficient for value in adult_nutrient_min_list]

        adult_nutrient_min_list[0] = self.dog_mer
        # 탄단지 비율 계산 쉽게 조정 
        adult_nutrient_min_list[1] = round(0.4 * self.dog_mer / 4,2)
        adult_nutrient_min_list[2] = round(0.1 * self.dog_mer / 9,2)
        adult_nutrient_min_list[3] = round(0.5 * self.dog_mer / 4,2)
        
        #aim_nut_list = [code, min, max] 구조 변화
        for i, code in enumerate(select_list):
            nutrient_value_max = adult_nutrient_max_list[i]
            nutrient_value_min = adult_nutrient_min_list[i]
            self.aim_nut_list.append([code, nutrient_value_min, nutrient_value_max])
        print('self.aim_nut_list', self.aim_nut_list)
    
    def food_variables(self):
        print('food_variables')
        self.foods = []
        for item in self.input_data:
            if item[1] != 0:
                food = self.solver.NumVar(item[1]/100, self.solver.infinity(), item[0])
            else:
                food = self.solver.NumVar(0.0, self.solver.infinity(), item[0])
            self.foods.append(food)
        print('self.foods', self.foods)
    
    def checking_constraints(self):
        print('checking_constraints')
        self.constraints = []
        # print(self.aim_nut_list)
        for i, nutrient in enumerate(self.aim_nut_list):
            if nutrient[2] != 0:
                self.constraints.append(self.solver.Constraint(nutrient[1], nutrient[2]))
            else:
                self.constraints.append(self.solver.Constraint(nutrient[1], self.solver.infinity()))
            for j, item in enumerate(self.user_food_nut_range):
                self.constraints[i].SetCoefficient(self.foods[j], item[i + 1])
        print('Number of constraints =', self.solver.NumConstraints())
                
    def macro_calcurate(self):
        self.calories_cal() # dog_nut checking
        self.solver_gen() # slover generator
        self.food_variables() # food variables
        self.checking_constraints() # constraints
                
    def step1(self): # calculate_recipe
        print('step1 start')
        nutrient_list = self.user_food_nut_range
        
        self.macro_calcurate() # 한번에 실행

        # Objective function
        objective = self.solver.Objective()
        for index, food in enumerate(self.foods):
            # 계수에 맞춰 읍식물 출력시 곱해줘야하는데 안해줘서 오류가 난것 같습니다.
            # coefficient = 50 if index < 2 else 100  # 첫 번째 음식의 계수를 100으로, 나머지는 1로 설정
            objective.SetCoefficient(food, 100)
        objective.SetMinimization()

        if not self.solver_check(): # problem check
            return 0

        self.calculated_recipe = []
        nutrients_result = [0] * len(nutrient_list)

        print('food', self.foods)
        for i, food in enumerate(self.foods):
            if food.solution_value() > 0.0:
                self.calculated_recipe.append((self.user_food_nut_range[i][0], round(100 * food.solution_value())))
                for j, _ in enumerate(nutrient_list):
                    nutrients_result[j] += self.user_food_nut_range[i][j + 1] * food.solution_value()
        print('step1 end')
        self._set_calculations()
        return self.calculated_recipe
    
    def step2(self):
        data = self.input_data # 식재료 이름, 영양소 코드
        nutrients = self.aim_nut_list
        
        self.macro_calcurate() # 한번에 실행

        # Objective function: Minimize the sum of (gram-normalized) foods
        objective = self.solver.Objective()
        for food in self.foods:
            objective.SetCoefficient(food, 100)
        objective.SetMinimization()

        self.solver_check()
    
        self.calculated_recipe = []
        # Display the amounts (in 100 grams) to purchase of each food.
        nutrients_result = [0] * len(nutrients)
        print('\n식재료 무게:')
        for i, food in enumerate(self.foods):
            if food.solution_value() > 0.0:
                self.calculated_recipe.append((data[i][0],math.ceil(100 * food.solution_value())))
                print('{}: {}'.format(data[i][0], 100. * food.solution_value()))
                for j, _ in enumerate(nutrients):
                    nutrients_result[j] += data[i][j + 1] * food.solution_value()
        return self.calculated_recipe
    
    def nut_report(self):
        self.result_nutrients = [0 for _ in range(132)]
        for result_food in self.calculated_recipe:
            for input_nut in self.user_food_nut_all:
                if input_nut[0] == result_food[0]:
                    div_num = input_nut[1]
                    self.result_nutrients = [round(a + (float(b) / div_num * result_food[1]), 2) for a, b in zip(self.result_nutrients, input_nut[1:])]
        print(len(self.result_nutrients))
        self.nut_some = [self.result_nutrients[16], self.result_nutrients[18], self.result_nutrients[22]]
        return self.result_nutrients[:7]
    
    def _set_calculations(self):
        need_nut = Need_Nut(self.dog_mer)
        self.max_cal = need_nut.need_max_mer()
        self.min_cal = need_nut.need_min_mer()
        
    def get_nut_some(self):
        return self.nut_some
    
    def get_nut_7(self):
        return sum(1 for nutrient, max_val in zip(self.result_nutrients, self.max_cal) if nutrient >= max_val)

    def process_nutrients(self):
        report_data = []
        for i, (nutrient, max_val, min_val) in enumerate(zip(self.result_nutrients, self.max_cal, self.min_cal)):
            range_val = max_val - min_val

            if range_val == 0:
                percent = 100 if nutrient > 0 else 0
            else:
                percent = round(((nutrient - min_val) / range_val), 3) * 100
                percent = min(max(percent, 0), 100)

            report_data.append((i, min_val, percent, nutrient))

        report_index, report_minimum, report_percent, report_actual = zip(*report_data) if report_data else ([], [], [], [])
        return report_index, report_minimum, report_percent, report_actual
    


    
class Need_Nut:
    def __init__(self, mer):
        self.mer_min = mer
        self.mer_max = mer + 50
        
    def need_max_mer(self):
        full_max_nutrient = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            4500, 0, 0, 4000, 0, 0, 0, 0, 0, 500, 0, 2750, 18750,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18.75,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0
        ]
        max_nutrient = [
            0, 0, 0, 0, 0, 0, 0, 0, 4500, 0, 0, 4000, 0, 0, 0, 0,
            0, 500, 0, 2750, 18750, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18.75, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        
        max_nutrient[0] = self.mer_max
        max_nutrient[1] = self.mer_max * 0.4
        max_nutrient[2] = self.mer_max * 0.2
        max_nutrient[3] = self.mer_max * 0.4
        return max_nutrient
    
    def need_min_mer(self):
        full_min_nutrient = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            1250, 10, 150, 1000, 1500, 200, 20, 1.83, 1.25, 80, 0, 250, 375,
            0, 0, 0.56, 1.3, 3.4, 0, 0, 0, 3, 0, 0.38, 0, 0, 54, 0, 7, 0, 3.125,
            0, 0, 8.39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 950, 1700, 1580, 830, 
            1130, 1200, 400, 1230, 480, 1280, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0, 0, 2800, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
            0, 0, 0, 0, 0
        ]
        min_nutrient = [
            0, 0, 0, 0, 0, 0, 0, 0, 1250, 10, 150, 1000, 1500, 200, 20, 1.83,
            1.25, 80, 0, 250, 375, 0.56, 1.3, 3.4, 3, 0, 0, 0, 7, 0, 3.125, 8.39,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        min_nutrient[0] = self.mer_min
        min_nutrient[1] = self.mer_min * 0.4
        min_nutrient[2] = self.mer_min * 0.2
        min_nutrient[3] = self.mer_min * 0.4
        return min_nutrient
    
# def nutrient_maker(min_caloric):
#     max_caloric = min_caloric + 50
#     protein_min_cal, fat_min_cal, carbohydrate_min_cal = min_caloric * 0.4 / 4, min_caloric * 0.2 / 9, min_caloric * 0.4 / 4
#     protein_max_cal, fat_max_cal, carbohydrate_max_cal = max_caloric * 0.4, max_caloric * 0.2, max_caloric * 0.4

#     nutrient_list = [['A10300', '단백질', 'g', protein_min_cal, 0], ['A10400', '지방 ', 'g', fat_min_cal, 0], ['A10600', '탄수화물', 'g', carbohydrate_min_cal, 0], ['A10100', '에너지', 'kcal', min_caloric, max_caloric]]
#     return nutrient_list
        
# if __name__ == '__main__':

    # data_list = []
    # diet_optimizer = DietOptimizer(data_list)
    # Food_db = 'db2.sqlite3'
    # conn = diet_optimizer.connect_db(Food_db)
    # input_list = diet_optimizer.get_input_list(conn, data_list)

    # min_caloric = DietOptimizer.caloric_generator(15)


    # calculated_recipe, nutrients_result = diet_optimizer.calculate_recipe(input_list)

    # print("Calculated Recipe:")
    # for item in calculated_recipe:
    #     print(f"{item[0]}: {item[1]}g")

    # print("\nNutrients Result:")
    # for i, nutrient in enumerate(nutrient_list):
    #     print(f"{nutrient[1]}: {nutrients_result[i]}{nutrient[2]} (min {nutrient[3]}, max {nutrient[4]})")
