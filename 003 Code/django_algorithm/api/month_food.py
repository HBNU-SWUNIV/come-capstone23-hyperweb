import random

class MenuGenerator:

    def __init__(self, main_food, sub_food):
        self.main_food = main_food
        self.sub_food = sub_food
        self.main_work_list = self.main_food
        self.sub_work_list = self.sub_food
        self.food_list = []
        self.unique_set = set()

    @staticmethod
    def generate_calories(is_main):
        if is_main:
            return random.randint(100, 200)
        else:
            return random.randint(10, 90)

    def generate(self, target_list_count=4):
        while len(self.food_list) < target_list_count:
            print(f'main_food rest :{self.main_work_list}')
            print(f'sub_food rest :{self.sub_work_list}')
            if len(self.main_work_list) or len(self.sub_work_list) < 1:
                # 작업 리스트를 원본 리스트로 다시 초기화합니다.
                self.main_work_list = self.main_food.copy()
                self.sub_work_list = self.sub_food.copy()

            main = random.choice(self.main_work_list)  # 메인 푸드를 무작위로 선택합니다.
            self.main_work_list.remove(main)  # 선택한 메인 푸드를 작업 리스트에서 제거합니다.

            sub_count = min(len(self.sub_work_list), 5)  # 남은 서브 푸드의 수와 5 중에서 더 작은 값을 선택합니다.
            chosen_subs = random.sample(self.sub_work_list, k=random.randint(2, sub_count))  # 서브 푸드를 2~5개 무작위로 선택합니다.

            for sub in chosen_subs:
                self.sub_work_list.remove(sub)  # 선택한 서브 푸드를 작업 리스트에서 제거합니다.

            # 메인과 서브 푸드에 칼로리 값을 부여합니다.
            food_combo = [(main, self.generate_calories(True))] + [(sub, self.generate_calories(False)) for sub in chosen_subs]
            combo_set = frozenset(food_combo)

            # 만약 생성한 조합이 중복이 아니라면 리스트에 추가합니다.
            if combo_set not in self.unique_set:
                self.food_list.append(food_combo)
                self.unique_set.add(combo_set)
            print(f'searching food : {self.food_list}')
        print(f'searching end ~!~!~!~!~!~~!~!~!~!~!~!~!!~!~1-----------------------')
        return self.food_list


# class MenuGenerator:
#     def __init__(self, main_food, sub_food):
#         self.main_food = main_food
#         self.sub_food = sub_food
#         self.food_list = []
#         self.unique_set = set()

#     @staticmethod
#     def generate_calories(is_main):
#         if is_main:
#             return random.randint(100, 200)
#         else:
#             return random.randint(10, 90)

#     def generate(self, target_list_count=4):
#         main_food_copy = self.main_food.copy()

#         while len(self.food_list) < target_list_count:
#             # 메인 푸드를 모두 사용했을 경우 초기화
#             if not main_food_copy:
#                 main_food_copy = self.main_food.copy()

#             main = random.choice(main_food_copy)
#             main_food_copy.remove(main)
            
#             if len(self.sub_food) < 2:
#                 sub_work_list = self.sub_food.copy()
#             else:
#                 sub_work_list = self.sub_food

#             sub_count = min(len(sub_work_list), 5)
#             chosen_subs = random.sample(sub_work_list, k=random.randint(2, sub_count))
#             for sub in chosen_subs:
#                 self.sub_food.remove(sub)
#                 if not self.sub_food:
#                     self.sub_food = self.sub_food.copy()

#             food_combo = [(main, self.generate_calories(True))] + [(sub, self.generate_calories(False)) for sub in chosen_subs]
#             combo_set = frozenset(food_combo)

#             if combo_set not in self.unique_set:
#                 self.food_list.append(food_combo)
#                 self.unique_set.add(combo_set)
#             print(f'searching food : {self.food_list}')

#         print(f'searching end -----------------------')
#         return self.food_list