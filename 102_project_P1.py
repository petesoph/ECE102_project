import sys
import pandas as pd


# Help function
def user_help():
    with open("user_guide.txt", 'r') as fin:
        print(fin.read())
    fin.close()


# Closes the program
def close_terminal():
    print("Goodbye")
    sys.exit()


# Checks sensors
def sensor_check(sensor_data_check):
    print(sensor_data_check)
    usr_input = input('Enter any key to return to main menu: ')
        

# Trigger individual sensors if armed
# This is for user wanting to trigger the sensors
def usr_sensor_trigger(sensor_data_func2, armed_state_func2, alarm_state_func2):
    # Only runs if alarm is armed (1 = armed, 0 = unarmed)
    tries = 0
    if armed_state_func2 == 1:
        # Asks for sensor ID, checks if it is a sensor
        usr_sensor = input("Enter the ID of the sensor to be checked: ")
        while usr_sensor not in sensor_data_func2[0] and tries < 5:
            usr_sensor = input("Please enter the ID of a sensor: ")
            tries += 1
        # For each sensor, 1 = triggered, 0 = not triggered
        # For alarm, 1 = ON, 0 = OFF
        if tries < 5:
            index = sensor_data_func2[0].index(usr_sensor)
            sensor_data_func2[index][0] = 1
            alarm_state_func2 = 1
        else:
            print("Out of tries!")
        # This will only check one sensor
        # It is better to have a loop in the main body to ask if another sensor needs to be checked
    else:
        print("Cannot check sensors, alarm not armed")
    # Returns updated sensor array and updated alarm state
    return sensor_data_func2, alarm_state_func2


# Triggering the sensor activates alarm if armed:
# This is more for hardware connections
def alarm_activate(sensor_data_func3, armed_state_func3, alarm_state_func3):
    # First check if armed (1 = armed, 0 = not armed)
    if armed_state_func3 == 1:
        for a in sensor_data_func3:
            sensor_state = sensor_data_func3.get(a)
            if sensor_state == 1:
                alarm_state_func3 = 1
    else:
        print("Cannot activate alarm, alarm not armed")
    # Returns alarm state (no changes made to dictionary or armed state)
    return alarm_state_func3


# Check if alarm is armed, arm if needed
def arm_alarm(armed_state_func4):
    # If alarm is off, user can arm
    if armed_state_func4 == 0:
        usr_entry = input("The alarm is not armed. Would you like to arm it? (Y/N): ")
        if usr_entry == 'Y' or usr_entry == 'y':
            # Give user 3 tries to enter passcode
            pass_entry = input("Please enter the passcode: ")
            tries = 1
            if pass_entry != "0451":
                while pass_entry != "0451" and tries < 3:
                    pass_entry = input("Incorrect. Please enter the passcode: ")
                    tries += 1
            if tries < 3:
                armed_state_func4 = 1
            else:
                print("Out of tries")
    else:
        usr_entry = input("The alarm is armed. Would you like to disarm it? (Y/N): ")
        if usr_entry == 'Y' or usr_entry == 'y':
            # Give user 3 tries to enter passcode
            pass_entry = input("Please enter the passcode: ")
            tries = 1
            if pass_entry != "0451":
                while pass_entry != "0451" and tries < 3:
                    pass_entry = input("Incorrect. Please enter the passcode: ")
                    tries += 1
            if tries < 3:
                armed_state_func4 = 0
            else:
                print("Out of tries")

    # Then return armed state
    return armed_state_func4


# Checks lights
def light_check(light_data_func5):
    print(light_data)
    user_input = input('Enter any key to return to main menu: ')


# Turns lights off/on
def light_off_on(light_data_vals):
    light_name = input("Reference list: outdoor, room1, room2, room3. \nPlease enter the name of the light: ")
    while light_name not in light_data_vals:
        light_name = input("Ivalid input. Please enter an existing light name: ")
    # 1 = ON, 0 = OFF
    if light_data_vals.get(light_name) == 1:
        lights_y_n = input("The light is ON. Would you like to turn it OFF? (Y/N): ")
        while lights_y_n not in {'Y', 'y', 'N', 'n'}:
            print('Invalid input, try again.')
            lights_y_n = input("The light is ON. Would you like to turn it OFF? (Y/N): ")
        if lights_y_n == 'Y' or lights_y_n == 'y':
            light_data.update({light_name, 0})
    else:
        lights_y_n = input("The light is OFF. Would you like to turn it ON? (Y/N): ")
        while lights_y_n not in {'Y', 'y', 'N', 'n'}:
            print('Invalid input, try again.')
            lights_y_n = input("The light is ON. Would you like to turn it OFF? (Y/N): ")
        if lights_y_n == 'Y' or lights_y_n == 'y':
            light_data.update({light_name, 1})
    return light_data


# Opens the trapdoor for a specific prisoner

def prisoner_trapdoor(prisoner_or_cell_number, cells_prisoners):
    # Calls function to get the index
    # Updates the prisoner's cell...to empty
    index_val = check_cell(prisoner_or_cell_number, cells_prisoners, 0)
    if index_val != -1000:
        cells_prisoners[index_val][1] = 0
        print(f"Prisoner number {cells_prisoners[index_val][1]} in cell number {cells_prisoners[index_val][0]}"
              f" has been trapdoored")
    else:
        print("Invalid prisoner or cell number")
        return cells_prisoners


def guard_trapdoor():
    # Displays a message and exits the program
    print("Guard is trapdoored")
    close_terminal()


# Possible option for prison riot/escape
# Just arms alarm and sets it off
def panic_button(arm_val, alarm_act_val):
    arm_val = alarm_act_val = 1
    return arm_val, alarm_act_val


def check_cell(cell_pris_num, cell_array_function1, print_flag):
    flag = 0
    # Set index to -1000, will be flag in other functions
    ret_index = -1000
    # First check based on prisoner number (always 3 digits)
    if cell_pris_num > 99:
        for index in range((len(cell_array_function1[:, 0]) - 1)):
            if cell_array_function1[index][1] == cell_pris_num:
                flag = 1
                if print_flag == 1:
                    print(f"Prisoner number {cell_pris_num} is in cell {cell_array_function1[index][0]}")
                    ret_index = index
                break
        if flag == 0:
            print(f"Prisoner number {cell_pris_num} not found")
            # Sets index to some invalid number
    # Then check based on cell number:
    else:
        for index in range((len(cell_array_function1[:, 0]) - 1)):
            if cell_array_function1[index][0] == cell_pris_num:
                flag = 1
                if print_flag == 1:
                    print(f"Cell number {cell_pris_num} holds prisoner number {cell_array_function1[index][1]}")
                    ret_index = index
                break
        if flag == 0:
            print(f"Cell number {cell_pris_num} not found")
    return ret_index


def update_cell(cell_prisoner_num, cell_array_function2, update_val):
    # First call function to get index
    index_num = check_cell(cell_prisoner_num, cell_array_function2, 0)
    if index_num != -1000:
        if update_val > 0:
            if update_val > 99:
                cell_array_function2[index_num][1] = update_val
            else:
                cell_array_function2[index_num][0] = update_val
        else:
            print("Invalid update value")
    else:
        print("Prisoner or cell not found, cannot update")
    return cell_array_function2


def valid_num():
    try:
        usr_input = int(input('Enter number here: '))
        print()
        
        while usr_input < 0 or usr_input > 7:
            print('Invalid input. Try again.')
            print()
            usr_input = int(input('Enter number here: '))
            
        if usr_input == 1:
            sensor_check(sensor_data)
        elif usr_input == 2:
            usr_sensor_trigger(sensor_data, armed_state, alarm_state)
        elif usr_input == 3:
            light_check(light_data)
        elif usr_input == 4:
            light_off_on(light_data)
        elif usr_input == 5:
            arm_alarm(armed_state)
        elif usr_input == 6:
            arm_alarm(armed_state)
        elif usr_input == 7:
            user_help()
        elif usr_input == 0:
            close_terminal()
            help()
    except ValueError:
        print('Invalid input. Try again.')
        print()
        valid_num()      
        

# Then this is the main menu of the program:
sensor_data = pd.DataFrame(
    data=[["Windows", 0], ["Main Door", 0], ["Cell 1", 0], ["Cell 2", 0], ["Cell 3", 0]],
    columns=['Sensor location', 'Status'])
light_data = pd.DataFrame(
    data=[["Main Light", 1], ["Main Light", 1], ["Main Light", 1]],
    columns=['Light location', 'Status'])
# Cell array entry is [cell #, prisoner #], w/ prisoner number == 0 => cell is empty
cell_data = pd.DataFrame(
    data=[[1, 123], [2, 350], [3, 0]],
    columns=['Cell location', 'Status'])

armed_state = 0
alarm_state = 0

print()
print('Hello, welcome to HADES:') 
print('Home Assistant (Defense and Extermination System)')
print()
print('Before you can access the main menu,')
password = str(input('please enter the password: '))

attempts = 2

while attempts >= 0:
    if password == '0451':
        break
    elif attempts > 0:
        attempts -= 1
        print()
        print(f'Incorrect password. {attempts + 1} attempts remaining.')
        password = str(input('please enter the password: '))
    else:
        print()
        print('Password attempt limit reached...')
        print('BON VOYAGE!')
        guard_trapdoor()
        sys.exit()  


while True:
    print()
    print('Welcome. Press the corresponding numbers to access HADES controls.')
    print()
    print('    -------------------- Main Menu ---------------------\n \
    1) Check sensors         | 5) Check if armed   \n \
    2) Trigger sensors       | 6) Arm/disarm       \n \
    3) Check lights          | 7) Help             \n \
    4) Turn lights off/on    | 0) Exit                 ')
    
    valid_num()
