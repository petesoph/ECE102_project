import sys
import numpy as np

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
def sensor_check(sensor_array_func1):
    print(f"Sensor ID   Sensor State")
    for a in sensor_array_func1:
        print(f"{sensor_array_func1[a][0]:<12}{sensor_array_func1[a][1]}")


# Trigger individual sensors if armed
# This is for user wanting to trigger the sensors
def usr_sensor_trigger(sensor_array_func2, armed_state_func2, alarm_state_func2):
    # Only runs if alarm is armed (1 = armed, 0 = unarmed)
    tries = 0
    if armed_state_func2 == 1:
        # Asks for sensor ID, checks if it is a sensor
        usr_sensor = input("Enter the ID of the sensor to be checked: ")
        while usr_sensor not in sensor_array_func2[0] and tries < 5:
            usr_sensor = input("Please enter the ID of a sensor: ")
            tries += 1
        # For each sensor, 1 = triggered, 0 = not triggered
        # For alarm, 1 = ON, 0 = OFF
        if tries < 5:
            index = sensor_array_func2[0].index(usr_sensor)
            sensor_array_func2[index][0] = 1
            alarm_state_func2 = 1
        else:
            print("Out of tries!")
        # This will only check one sensor
        # It is better to have a loop in the main body to ask if another sensor needs to be checked
    else:
        print("Cannot check sensors, alarm not armed")
    # Returns updated sensor array and updated alarm state
    return sensor_array_func2, alarm_state_func2


# Triggering the sensor activates alarm if armed:
# This is more for hardware connections
def alarm_activate(sensor_array_func3, armed_state_func3, alarm_state_func3):
    # First check if armed (1 = armed, 0 = not armed)
    if armed_state_func3 == 1:
        for a in sensor_array_func3:
            sensor_state = sensor_array_func3.get(a)
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
def light_check(light_array_func5):
    print(f"Light ID   Light State")
    for a in light_array_func5:
        print(f"{light_array_func5[a][0]:<12}{light_array_func5[a][1]}")


# Turns lights off/on
def light_off_on(light_array_func6):
    tries = 0
    light_name = input("Please enter the name of the light: ")
    while light_name not in light_array_func6[0] and tries < 5:
        light_name = input("Please enter the ID of a sensor: ")
        tries += 1
    if tries < 5:
        index = light_array_func6[0].index(light_name)
        if light_array_func6[index][0] == 'ON':
            lights_y_n = input("The light is ON. Would you like to turn it OFF? (Y/N): ")
            if lights_y_n == 'Y' or lights_y_n == 'y':
                light_array_func6[index][0] = 'OFF'
        else:
            lights_y_n = input("The light is OFF. Would you like to turn it ON? (Y/N): ")
            if lights_y_n == 'Y' or lights_y_n == 'y':
                light_array_func6[index][0] = 'ON'
    return light_array_func6


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


# Then this is the main menu of the program:
sensor_array = np.array([["Windows", 0], ["Main Door", 0], ["Cell 1", 0], ["Cell 2", 0], ["Cell 3", 0]])
# TODO: change these two so they read from a file
light_array = np.array([["Main Light", "ON"], ["Main Light", "ON"], ["Main Light", "ON"]])
# Cell array entry is [cell #, prisoner #], w/ prisoner number == 0 => cell is empty
cell_array = np.array([[1, 123], [2, 350], [3, 0]])
armed_state = 0
alarm_state = 0

while True:
    print("Main Menu\nOptions:")
    print("Option 1: Check sensors\nOption 2: Trigger sensors")
    print("Option 3: Check lights\nOption 4: Turn lights off/on")
    print("Option 5: Check if armed\nOption 6: Arm/disarm")
    print("Enter 7 for help, enter 0 to exit")
    input_flag = 0
    usr_input = input("Please enter the # of the option you want: ")
    while input_flag == 0:
        if usr_input == '1':
            sensor_check(sensor_array)
        elif usr_input == '2':
            sensor_array, alarm_state = usr_sensor_trigger(sensor_array, armed_state, alarm_state)
        elif usr_input == '3':
            light_check(light_array)
        elif usr_input == '4':
            light_array = light_off_on(light_array)
        elif usr_input == '5':
            armed_state = arm_alarm(armed_state)
        elif usr_input == '6':
            armed_state = arm_alarm(armed_state)
        elif usr_input == '7':
            user_help()
        elif usr_input == '0':
            close_terminal()
        else:
            input_flag = 0
            usr_input = input("Please enter a valid input: ")
        input_flag += 1
