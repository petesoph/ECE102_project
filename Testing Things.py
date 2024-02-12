import pandas as pd
import numpy as np

light_data = pd.DataFrame(
    data=[["Outdoor", 1], ["Cell 1", 1], ["Cell 2", 1], ['Cell 3', 1]],
    columns= ['Light location', 'Status'])

#light_name = 'Cell 1'
#location = np.where(light_data == light_name)
#row_index, column_index = int(location[0]), int(location[1] + 1)
#print(light_data.iloc[row_index, column_index])
#light_data.iloc[row_index, column_index] = 0

#print(light_data)

# Turns lights off/on
def light_off_on(light_data):
   light_name = input("Reference list: Outdoor, Cell 1, Cell 2, Cell 3. \n \
Please enter the name of the light: ")
   while light_name not in light_data['Light location'].tolist():
       print() 
       light_name = input("Ivalid input. Please enter an existing light name: ")
   # 1 = ON, 0 = OFF
   location = np.where(light_data == light_name)
   row_index, column_index = int(location[0]), int(location[1] + 1)
   
   if light_data.iloc[row_index, column_index] == 1:
       lights_y_n = input("The light is ON. Would you like to turn it OFF? (Y/N): ")
       while lights_y_n not in {'Y', 'y', 'N', 'n'}:
           print()
           print('Invalid input, try again.')
           lights_y_n = input("The light is ON. Would you like to turn it OFF? (Y/N): ")
       if lights_y_n == 'Y' or lights_y_n == 'y':
           light_data.iloc[row_index, column_index] = 0
   else:
       lights_y_n = input("The light is OFF. Would you like to turn it ON? (Y/N): ")
       while lights_y_n not in {'Y', 'y', 'N', 'n'}:
           print()
           print('Invalid input, try again.')
           lights_y_n = input("The light is ON. Would you like to turn it OFF? (Y/N): ")
       if lights_y_n == 'Y' or lights_y_n == 'y':
           light_data.iloc[row_index, column_index] = 1
   return light_data

light_off_on(light_data)