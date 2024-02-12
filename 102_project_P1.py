import sys
import numpy as np
import pandas as pd

# Rough working copy
# Changed dictionaries to arrays
# Added some places for extra features

# Req. features:
# help command prints instructions for terminal
# exit command closes python script cleanly
# Able to check state of sensors
# Able to trigger individual sensors
# Triggering sensor activates alarm (only when armed)
# Able to check state of lights
# Able to turn lights off/on
# Able to check if alarm is armed
# Able to arm alarm with the passcode 0451

# Optional features (need ideally 6)
# Simulate/control lights for multiple rooms
# Option to change passcode
# Simulate 'more ambitious device'
# Remember light state when open/close program

# Other optional feature options
# Trapdoor for prisoners
# Trigger guard trapdoor after password tries is maxed out
# Guard login/logout
# Check/update prisoner number for a cell
# Allow a visitor into the prison
# Anything else

# General todo:
# Change lights to read/write from/to file
# Fill in extra functions
# Check that functions are correctly connected to each other (e.g. 5 password fails => call guard trapdoor function)
# Update main program menu (once functions are finalized)
# Write user manual (once everything else is finalized)


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
def sensor_check(sensor_data):
    print (sensor_data)
    
    user_input = []

    while user_input == []:
        print()
        print('Enter any key to return to main menu: ')
        user_input = [str(input())]
    
        

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
    
    user_input = []

    while user_input == []:
        print()
        print('Enter any key to return to main menu: ')
        user_input = [str(input())]


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
           lights_y_n = input("The light is OFF. Would you like to turn it ON? (Y/N): ")
       if lights_y_n == 'Y' or lights_y_n == 'y':
           light_data.iloc[row_index, column_index] = 1
   return light_data


# Other functions
def prisoner_trapdoor(prisoner_number):
    # Opens the trapdoor for a specific prisoner
    # Should also call a function from here to update the prisoner's cell...to empty
    pass


def guard_trapdoor():
    # Can call this if the guard does not remember his password 3x
    # Maybe also have this one display a message and quit the program, as the guard will no longer be using it
    pass


def admit_visitor():
    # Lets the guard unlock the door so someone can visit the prison
    pass


def check_cell(cell_array_function1):
    # Should open file w/ prisoner numbers (possible w/ saved numpy array? if not can just use .txt)
    # Should prompt for cell number or prisoner number
    # Then say either what prisoner/what cell
    pass


def update_cell(cell_array_function2, cell_num, trapdoor_flag):
    # This function will be used either to manually update cell info or automatically after trapdoor
    # So use trapdoor_flag to know if it is the manual (user input) option or the automatic option
    pass


def panic_button():
    # Possible option for prison riot/escape?
    pass

    
    
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
    data= [["Windows", 0], ["Main Door", 0], ["Cell 1", 0], ["Cell 2", 0], ["Cell 3", 0]],
    columns= ['Sensor location', 'Status'])
# TODO: change these two so they read from a file
light_data = pd.DataFrame(
    data=[["Outdoor", 1], ["Cell 1", 1], ["Cell 2", 1], ['Cell 3', 1]],
    columns= ['Light location', 'Status'])
# Cell array entry is [cell #, prisoner #], w/ prisoner number == 0 => cell is empty
cell_data = pd.DataFrame(
    data= [[1, 123], [2, 350], [3, 0]],
    columns= ['Cell location', 'Status'])

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
        guard_trapdoor(0)
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
