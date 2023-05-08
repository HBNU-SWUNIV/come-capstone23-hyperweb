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
            user_input = data["name"]
            searching_food_db = searching_food_db_template.format(user_input)

            cursor.execute(searching_food_db)
            result = cursor.fetchone()
            temp = list(result)
            del temp[0:2]
            temp.pop(1)
            input_list.append(temp)

        cursor.close()
        conn.close()

        return input_list





    def calculate_recipe(self, input_list):
        nutrient_list = []
        min_caloric_val = caloric_generator(self)

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
                exit(1)

        calculated_recipe = []
        nutrients_result = [0] * len(nutrient_list)

        for i, food in enumerate(foods):
            if food.solution_value() > 0.0:
                calculated_recipe.append((input_list[i][0], round(100 * food.solution_value())))
                for j, _ in enumerate(nutrient_list):
                    nutrients_result[j] += input_list[i][j + 1] * food.solution_value()

        result_list = [0 for _ in range(132)]
        for i in range(len(input_list)):
            temp = [float(x) * 0.01 * float(calculated_recipe[i][1]) for x in input_list[i][1:]]
            result_list = result_list + temp[1:]

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(calculated_recipe, f, ensure_ascii=False, indent=4)

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result_list, f, ensure_ascii=False, indent=4)
            
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
    # protein_max_cal, fat_max_cal, carbohydrate_max_cal = max_caloric * 0.4, max_caloric * 0.2, max_caloric * 0.4

    nutrient_list = [['A10300', '단백질', 'g', protein_min_cal, 0], ['A10400', '지방 ', 'g', fat_min_cal, 0], ['A10600', '탄수화물', 'g', carbohydrate_min_cal, 0], ['A10100', '에너지', 'kcal', min_caloric, max_caloric]]
    return nutrient_list


if __name__ == '__main__':
    # nutrient_list = []
    # min_caloric = caloric_generator
    # '[{"name": "돼지고기, 등심, 생것", "unit": "0"}, {"name": "달걀, 생것", "unit": "0"}, {"name": "멥쌀, 백미, 밥", "unit": "0"}, {"name": "고구마, 생것", "unit": "0"}, {"name
    # nutrient_list = nutrient_maker(min_caloric)
    # 입력을 받아서 data_list를 생성합니다.
    print("Please input the data_list as a JSON string:")
    json_data = input()
    data_list = json.loads(json_data)
    
    diet_optimizer = DietOptimizer(data_list)
    db_file = 'db2.sqlite3'
    conn = diet_optimizer.connect_db(db_file)
    input_list = diet_optimizer.get_input_list(conn, data_list)

    # min_caloric = DietOptimizer.caloric_generator(15)


    calculated_recipe, nutrients_result = diet_optimizer.calculate_recipe(input_list)

    print("Calculated Recipe:")
    for item in calculated_recipe:
        print(f"{item[0]}: {item[1]}g")

    print("\nNutrients Result:")
    for i, nutrient in enumerate(nutrient_list):
        print(f"{nutrient[1]}: {nutrients_result[i]}{nutrient[2]} (min {nutrient[3]}, max {nutrient[4]})")
