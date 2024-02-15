import sys
import os.path as path


# File opener function (to open saved light info and cell info)
# Checks if file exists, if not, sets all lights ON or empty cells
# If file exists, reads from file, stores in arrays
def file_checker(file_name, default_array):
    # First check if the file exists:
    if path.isfile(file_name):
        with open(file_name, 'r') as f:
            temp_list = f.readlines()
            # Double checks that the list isn't empty:
            if temp_list:
                n = 0
                for line in temp_list:
                    line_list = line.split(':')
                    default_array[n][0] = line_list[0] + ':'
                    default_array[n][1] = line_list[1].strip('\n')
                    n += 1
            else:
                print("No info in file, returning defaults")
    else:
        # If file doesn't exist, will make the file
        f = open(file_name, 'r')
        print("Can't find file, returning defaults")
    f.close()
    return default_array


# Also need to write to file before closing the program:
def file_writer(sensors_info, lights_info, cells_info):
    global file_names_tuple
    # Sensors info
    f = open(file_names_tuple[0], 'w')
    for entry in sensors_info:
        f.write(f"{entry[0]}{entry[1]}\n")
    f.close()
    # Lights info
    f = open(file_names_tuple[1], 'w')
    for entry in lights_info:
        f.write(f"{entry[0]}{entry[1]}\n")
    f.close()
    # Cells info
    f = open(file_names_tuple[2], 'w')
    for entry in cells_info:
        f.write(f"{entry[0]}{entry[1]}\n")
    f.close()


# Help function
def user_help():
    with open("user_guide.txt", 'r') as fin:
        print(fin.read())
    fin.close()


# Closes the program; all program closes should go through this function (so there is no sys.exit() at program end)
def close_terminal(sensors, lights, cells):
    # First updates the files
    file_writer(sensors, lights, cells)
    print("Goodbye")
    sys.exit()


# Checks sensors
def sensor_check(sensor_data_check):
    print("Sensor ID   Sensor State")
    for n in range(len(sensor_data_check)):
        print(f"{sensor_data_check[n][0]:<12}{sensor_data_check[n][1]}")
    print()
    input('Enter any key to return to main menu: ')
        

# Trigger individual sensors if armed
# This is for user wanting to trigger the alarm through an individual sensor
def usr_sensor_trigger(sensor_data_func2, armed_state_func2, alarm_state_func2):
    # Only runs if alarm is armed (1 = armed, 0 = unarmed)
    tries = 0
    if armed_state_func2 == 1:
        # Asks for sensor ID, checks if it is a sensor
        print('Reference list: \'Windows:\', \'Main Door:\', \'Cell 1:\', \'Cell 2:\', \'Cell 3:\', \'Metal Detector:\'')
        usr_sensor = input("Enter the ID of the sensor to be triggered: ")
        while tries < 5:
            if any(usr_sensor == sensor[0] for sensor in sensor_data_func2):
                break
            usr_sensor = input("Please enter the ID of a sensor: ")
            tries += 1

        if tries < 5:
            print()
            alarm_activate(armed_state, alarm_state)

        else:
            print("Out of tries!")
            print()
            input('Enter any key to return to main menu: ')
    else:
        print("Cannot trigger sensors, alarm not armed")
        print()
        input('Enter any key to return to main menu: ')
    # Returns updated sensor array and updated alarm state
    return sensor_data_func2, alarm_state_func2


# Triggering the sensor activates alarm if armed:
# May change this
def alarm_activate(armed_state_func3, alarm_state_func3):
    # First check if armed (1 = armed, 0 = not armed)
    global alarm_state
    if armed_state_func3 == 1:
        answer = input('Are you sure you wish to PANIC? (Y/N): ')
        print()
        if answer == 'y' or 'Y':
            print('WEEE WOOO WEEE WOOO WEEE...')
            alarm_state = 1
    else:
        print("Cannot activate alarm, alarm not armed")
        print()
        input('Enter any key to return to main menu')
    # Returns alarm state
    return alarm_state_func3


# Check if alarm is armed, arm if needed
def arm_alarm(armed_state_func4, sensor, light, cell):
    # If alarm is off, user can arm
    global armed_state
    global alarm_state
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
                armed_state = 1
            else:
                # Password failure triggers guard trapdoor
                print("Out of tries")
                guard_trapdoor(sensor, light, cell)
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
                armed_state = 0
                alarm_state = 0
            else:
                # Password failure triggers guard trapdoor
                print("Out of tries")
                guard_trapdoor(sensor, light, cell)
    # Then return armed state
    return armed_state_func4


# Checks lights
def light_check(light_data_func5):
    print("Light Name\t\tON/OFF")
    for n in range(len(light_data_func5)):
        print(f"{light_data_func5[n][0]}\t\t{light_data_func5[n][1]}")
    # Waits for user input to close
    input('Enter any key to return to main menu: ')


# Turns lights off/on
def light_off_on(light_data_vals):
    print("Reference list: \'Main Light:\', \'Cell 1:\', \'Cell 2:\', \'Cell 3:\'")
    light_name = input("Please enter the name of the light: ")
    tries = 0
    # Give 3 tries, then end loop
    while tries < 3:
        if any(light_name == light[0] for light in light_data_vals):
            break
        light_name = input("Invalid input. Please enter an existing light name: ")
        tries += 1
    if tries != 3:
        light_index = next(index for index, light in enumerate(light_data_vals) if light[0] == light_name)
        if light_data_vals[light_index][1] == "ON":
            lights_y_n = input("The light is ON. Would you like to turn it OFF? (Y/N): ")
            while lights_y_n not in {'Y', 'y', 'N', 'n'}:
                lights_y_n = input('Invalid input, try again.')
            if lights_y_n == 'Y' or lights_y_n == 'y':
                light_data_vals[light_index][1] = "OFF"
        else:
            lights_y_n = input("The light is OFF. Would you like to turn it ON? (Y/N): ")
            while lights_y_n not in {'Y', 'y', 'N', 'n'}:
                lights_y_n = input('Invalid input, try again.')
            if lights_y_n == 'Y' or lights_y_n == 'y':
                light_data_vals[light_index][1] = "ON"
    else:
        print("Out of tries, returning to menu")
    return light_data_vals


# Opens the trapdoor for a specific prisoner
def prisoner_trapdoor(prisoner_or_cell_number, cells_prisoners):
    # Calls function to get the index
    # Updates the prisoner's cell...to empty
    index_val = check_cell(prisoner_or_cell_number, cells_prisoners, 0)
    if index_val != -1000:
        cells_prisoners[index_val][1] = 0
        print(f"Prisoner number {cells_prisoners[index_val][1]} in cell number {cells_prisoners[index_val][0]}"
              f" has been trapdoor-ed")
    else:
        print("Invalid prisoner or cell number")
        return cells_prisoners


def guard_trapdoor(sensor_list, light_list, cell_list):
    # Displays a message and exits the program
    print("Guard is trapdoor-ed")
    close_terminal(sensor_list, light_list, cell_list)


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


def valid_num(sensor_data_menu, light_data_menu, cell_data_menu, armed_state_menu, alarm_state_menu):
    try:
        usr_input = int(input('Enter number here: '))
        print()
        
        while usr_input < 0 or usr_input > 7:
            print('Invalid input. Try again.')
            print()
            usr_input = int(input('Enter number here: '))
            
        if usr_input == 1:
            sensor_check(sensor_data_menu)
        elif usr_input == 2:
            usr_sensor_trigger(sensor_data_menu, armed_state, alarm_state)
        elif usr_input == 3:
            light_check(light_data_menu)
        elif usr_input == 4:
            light_off_on(light_data_menu)
        elif usr_input == 5:
            arm_alarm(armed_state_menu, sensor_data_menu, light_data_menu, cell_data_menu)
        elif usr_input == 6:
            alarm_activate(armed_state_menu, alarm_state_menu)
        elif usr_input == 7:
            user_help()
        elif usr_input == 0:
            close_terminal(sensor_data_menu, light_data_menu, cell_data_menu)
    except ValueError:
        print('Invalid input. Try again.')
        print()
        valid_num(sensor_data_menu, light_data_menu, cell_data_menu, armed_state_menu, alarm_state_menu)
        

# Default arrays (if no data is available)
default_sensor_data = [["Windows:", 0], ["Main Door:", 0], ["Cell 1:", 0], ["Cell 2:", 0], ["Cell 3:", 0], ["Metal Detector:", 0]]
default_light_data = [["Main Light:", "ON"], ["Cell 1:", "ON"], ["Cell 2:", "ON"], ["Cell 3:", "ON"]]
# Cell array entry is [cell #, prisoner #], w/ prisoner number == 0 => cell is empty
default_cell_data = [['1:', 123], ['2:', 350], ['3:', 0]]
armed_state = 0
alarm_state = 0

# Before program starts, checks if file data is available and updates lights/sensors/cells
# File names are:
file_names_tuple = ("sensors_file.txt", "lights_file.txt", "cells_file.txt")
sensor_data = file_checker("sensors_file.txt", default_sensor_data)
light_data = file_checker("lights_file.txt", default_light_data)
cell_data = file_checker("cells_file.txt", default_cell_data)


print('Hello, welcome to HADES:')
print('Home Assistant, Defense, and Extermination System')
print('Before you can access the main menu,')
password = input('please enter the password: ')

attempts = 2

while attempts >= 0:
    if password == '0451':
        break
    elif attempts > 0:
        attempts -= 1
        print(f'Incorrect password. {attempts + 1} attempts remaining.')
        password = input('please enter the password: ')
    else:
        # Password fail triggers guard trapdoor
        print('Password attempt limit reached...\nBON VOYAGE!')
        guard_trapdoor(sensor_data, light_data, cell_data)
        
# Then this is the main menu of the program:
while True:
    print('\nWelcome. Press the corresponding numbers to access HADES controls.\n')
    print('    -------------------- Main Menu ---------------------\n \
    1) Check sensors         | 5) Arm/disarm alarm \n \
    2) Trigger sensors       | 6) PANIC!       \n \
    3) Check lights          | 7) Help             \n \
    4) Turn lights off/on    | 0) Exit                 ')
    print(f'    ------------------ Alarm state: {alarm_state} ------------------')
    
    if armed_state == 1:
        for sensor in sensor_data:
            sensor[1] = '1'
    else:
        for sensor in sensor_data:
            sensor[1] = '0'

    valid_num(sensor_data, light_data, cell_data, armed_state, alarm_state)
    