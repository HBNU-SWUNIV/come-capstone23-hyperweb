import sqlite3
import json
from ortools.linear_solver import pywraplp


class DietOptimizer:
    def __init__(self, data_list):
        self.data_list = data_list
        # self.nutrient_list = nutrient_list

    def connect_db(self, db_file):
        conn = sqlite3.connect(db_file)
        return conn

    def get_input_list(self, conn, data_list):
        cursor = conn.cursor()
        input_list = list()

        for data in data_list:
            searching_food_db_template = "SELECT * FROM food_national WHERE name = '{}'"
            # user_input = data["name"]
            user_input = data[0]
            searching_food_db = searching_food_db_template.format(user_input)

            cursor.execute(searching_food_db)
            result = cursor.fetchone()
            temp = list(result)
            del temp[0:2]
            # temp.pop(1)
            del temp[1]
            input_list.append(temp)

        cursor.close()
        conn.close()

        return input_list
    def max_calcurate(self, max_cal):
        max_nutrient = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4500.0, 0.0, 0.0, 4000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 500.0, 0.0, 2750.0, 18750.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 18.75, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 30.0, 2.0]
        adult_nutrient = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1250.0, 10.0, 150.0, 1000.0, 1500.0, 200.0, 20.0, 1.83, 1.25, 80.0, 0.0, 250.0, 375.0, 0.0, 0.0, 0.56, 1.3, 3.4, 0.0, 0.0, 0.0, 3.0, 0.0, 0.38, 0.0, 0.0, 54.0, 0.0, 7.0, 0.0, 3.125, 0.0, 0.0, 8.39, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 950.0, 1700.0, 1580.0, 830.0, 1130.0, 1200.0, 400.0, 1230.0, 480.0, 1280.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2800.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        max_nutrient[0] = max_cal
        max_nutrient[1] = max_cal * 0.4
        max_nutrient[2] = max_cal * 0.2
        max_nutrient[3] = max_cal * 0.4
        return max_nutrient
    
    def min_calcurate(self, min_cal):
        min_nutrient = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3000.0, 22.0, 150.0, 2500.0, 1500.0, 800.0, 25.0, 3.1, 1.8, 90.0, 0.0, 250.0, 375.0, 0.0, 0.0, 0.56, 1.3, 3.4, 0.0, 0.0, 0.0, 3.0, 0.0, 0.38, 0.0, 0.0, 54.0, 0.0, 7.0, 0.0, 3.125, 0.0, 0.0, 8.39, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1780.0, 3230.0, 2250.0, 880.0, 2080.0, 2600.0, 500.0, 1700.0, 1100.0, 2500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3300.0, 200.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        min_nutrient[0] = min_cal
        min_nutrient[1] = min_cal * 0.4
        min_nutrient[2] = min_cal * 0.2
        min_nutrient[3] = min_cal * 0.4
        return min_nutrient

    def calculate_recipe(self, input_list, min_caloric_val):
        nutrient_list = []
        # min_caloric_val = caloric_generator(self)
        input_list_origin = input_list
        nutrient_list = nutrient_maker(min_caloric_val)
        # Instantiate a Glop solver and naming it.
        solver = pywraplp.Solver.CreateSolver('GLOP')
        if not solver:
            print('solver 오류')

        # Variables
        foods = []
        for item in input_list:
            if item[1] != 0:
                food = solver.NumVar(item[1]/100, solver.infinity(), item[0])
            else:
                food = solver.NumVar(0.0, solver.infinity(), item[0])
            foods.append(food)

        # Constraints
        constraints = []
        for i, nutrient in enumerate(nutrient_list):
            if nutrient[4] != 0:
                constraints.append(solver.Constraint(nutrient[3], nutrient[4]))
            else:
                constraints.append(solver.Constraint(nutrient[3], solver.infinity()))
            for j, item in enumerate(input_list):
                constraints[i].SetCoefficient(foods[j], item[i + 1])

        # Objective function
        objective = solver.Objective()
        for food in foods:
            objective.SetCoefficient(food, 100)
        objective.SetMinimization()

        status = solver.Solve()

        # Check solution
        if status != solver.OPTIMAL:
            print('The problem does not have an optimal solution!')
            if status == solver.FEASIBLE:
                print('A potentially suboptimal solution was found.')
            else:
                print('The solver could not solve the problem.')
                return 0,0

        calculated_recipe = []
        nutrients_result = [0] * len(nutrient_list)

        for i, food in enumerate(foods):
            if food.solution_value() > 0.0:
                calculated_recipe.append((input_list[i][0], round(100 * food.solution_value())))
                for j, _ in enumerate(nutrient_list):
                    nutrients_result[j] += input_list[i][j + 1] * food.solution_value()

        result_list = [0 for _ in range(132)]
        print('calculated_recipe', calculated_recipe)
        print(len(result_list))
        print(input_list_origin)
        for i, load in enumerate(input_list_origin):
            print('load', load)
            for j, x in enumerate(load[1:]):
                result_list[j] = round(result_list[j] + float(x) * 0.01 * float(calculated_recipe[i][1]), 2)
        print('result_list', result_list)
        # with open('data.json', 'w', encoding='utf-8') as f:
        #     json.dump(calculated_recipe, f, ensure_ascii=False, indent=4)

        # with open('data.json', 'w', encoding='utf-8') as f:
        #     json.dump(result_list, f, ensure_ascii=False, indent=4)
            
        return calculated_recipe, result_list

def caloric_generator(self):
    cal_weight = 1
    kg = 15

    MER = 132 * (kg ** 0.75)

    #input
    Neutered = True
    Obese = True
    activate = 2
    Anxious = True
    Senior = True
    if Neutered:
        cal_weight = cal_weight *0.75
    if Obese:
        cal_weight = cal_weight * 0.45
    if activate == 0:
        cal_weight = cal_weight * 0.72
    if activate == 1:
        cal_weight = cal_weight * 1.06
    if activate == 2:
        cal_weight = cal_weight * 1.36
    if Anxious:
        cal_weight = cal_weight * 1.2
    if Senior:
        cal_weight = cal_weight * 0.8

    calories = MER * cal_weight
    return round(calories)

    
def nutrient_maker(min_caloric):
    max_caloric = min_caloric + 50
    protein_min_cal, fat_min_cal, carbohydrate_min_cal = min_caloric * 0.4 / 4, min_caloric * 0.2 / 9, min_caloric * 0.4 / 4
    protein_max_cal, fat_max_cal, carbohydrate_max_cal = max_caloric * 0.4, max_caloric * 0.2, max_caloric * 0.4

    nutrient_list = [['A10300', '단백질', 'g', protein_min_cal, 0], ['A10400', '지방 ', 'g', fat_min_cal, 0], ['A10600', '탄수화물', 'g', carbohydrate_min_cal, 0], ['A10100', '에너지', 'kcal', min_caloric, max_caloric]]
    return nutrient_list


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
