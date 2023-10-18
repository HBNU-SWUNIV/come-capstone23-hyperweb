import sqlite3

class FoodSearch:
    def __init__(self):
        self.conn = None
        self.input_data = []

    def connect_db(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def close_db(self):
        if self.conn:
            self.conn.close()

    def get_input_list(self, input_data):
        if not self.conn:
            print("Database connection is not established.")
            return
        
        cursor = self.conn.cursor()
        input_list = []

        for data in input_data:
            searching_food_db_template =f"SELECT * FROM food_national WHERE name = '{data[0]}'"
            searching_food_db = searching_food_db_template
            cursor.execute(searching_food_db)
            result = cursor.fetchone()
            if result:  # If there is a result
                temp = list(result)
                del temp[0:2]
                del temp[1]
                input_list.append(temp)

        cursor.close()
        return input_list
    
    def get_calcurate_list(self, input_data):
        select_list = ['A10100','A10300','A10400',
                       'A10600','D10201','D10202',
                       'D10203','D10204','D10205',
                       'D10206','D10207','D10208',
                       'D10209','D10210']
        if not self.conn:
            print("Database connection is not established.")
            return
        
        cursor = self.conn.cursor()
        input_list = []
        for data in input_data:
            columns = ", ".join(select_list)
            
            searching_food_db_template = f"SELECT {columns} FROM food_national WHERE name = '{{}}'"
            user_input = data[0]
            searching_food_db = searching_food_db_template.format(user_input)
            cursor.execute(searching_food_db)
            result = cursor.fetchone()
            if result:  # If there is a result
                input_list.append([user_input]+list(result))

        cursor.close()
        return input_list
    
    def get_category_list(self, input_data):
        if not self.conn:
            print("Database connection is not established.")
            return
        
        cursor = self.conn.cursor()
        input_list = []

        for data in input_data:
            print(data[0])
            searching_food_db_template = f"SELECT category_group FROM food_national WHERE name = '{{}}'"
            user_input = data[0]
            searching_food_db = searching_food_db_template.format(user_input)
            cursor.execute(searching_food_db)
            result = cursor.fetchone()
            if result is None:
                input_list.append(None)
            elif result[0] == 'group8':
                print(result[0])
                input_list.append(True)
            else:
                print(result[0])
                input_list.append(False)
        cursor.close()
        return input_list