# Written by Scott Proctor
import serialConnect
import re
# NOTE to self: Current Problem: configuration_questions is not differentiating between what device was chosen

# Create a Device class to help reference various options and menus that are specific to the Device chosen
class Device:
    def __init__(self, device_type, configuration_questions, menu_options):
        self.device_type = device_type
        self.configuration_questions = configuration_questions
        self.menu_options = menu_options

    # First main function of the program is to create an initial config for the Device
    def start_configuration(self):
        print('-' * 42)
        print(f"Starting Initial Configuration Wizard...")  # Let the user know what is about to happen
        print('-' * 42)
        # Create an empty dictionary so that it can be added to easily if necessary
        startConfig = dict()
        ip_pattern = re.compile(r"^(10|172\.(1[6-9]|2\d|3[01])|192\.168)(\.\d{1,3}){3}$")
        # Create keys for the dictionary and have the input from the user be stored as the value
        while True:
            try:
                startConfig['hostname'] = input('Hostname: ')
                if not re.match(r'^[a-zA-Z0-9]{1,2}[a-zA-Z0-9-]*$', startConfig['hostname']):
                    if startConfig['hostname'][0] == '-':
                        raise ValueError ("Hostnames cannot start with a hyphen.")
                    else:
                        raise ValueError ("Hostnames cannot contain special characters except for hyphens (-).")
                break
            except ValueError as e: print(e)
        while True:
            try:
                startConfig['username'] = input('Username: ')
                if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', startConfig['username']):
                    if startConfig['username'][0].isdigit():
                        raise ValueError ('Username\'s must start with a letter.')
                    else:
                        raise ValueError ('Usernames cannot contain special characters except for underscores (_).')
                break
            except ValueError as e: print(e)
        while True:
            try:
                startConfig['password'] = input('Password: ')
                if len(startConfig['password']) < 10:
                    raise ValueError ('For security, passwords are recommended to be at least 10 characters long.')
                else:
                    break
            except ValueError as e: print(e)
        while True:
            try:
                #NOTE: The '.local' domain is known to create some issues with apple devices.  If your network requires
                # apple devices be connected, consider using a 'internal.yourdomain.com' format.
                startConfig['ipDomain'] = input('What domain name will you use?\n Examples: domainName.com or studentRack4.local\n')
                if not re.match(r'^(([a-zA-Z0-9-]+\.)*[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9](\.[a-zA-Z]{2,}))$', startConfig['ipDomain']):
                    raise ValueError ('Invalid Domain Name, try again.') 
                break
            except ValueError as e: print(e)
        while True:
            try:
                startConfig['manInt'] = input('What interface will remotely manage this device?\n Examples: G0/0/1 or Fa0/0/1\n')
                if not re.match(r'^(g|gi|fa)([0,1]+(/\d{1,2}){0,2})?$', startConfig['manInt'], re.IGNORECASE):
                    raise ValueError('Invalid interface format.  Please try again.')
                break
            except ValueError as e: print(e)
        while True:
            try:
                startConfig['manIp'] = input("And what will it's IP address be?\n Example: 192.168.1.1\n")
                if ip_pattern.match(startConfig['manIp']):
                    break
                raise ValueError('Invalid IP address. Only Private addressing schemes are accepted.')
            except ValueError as e: print(e)
        while True:
            try:
                startConfig['subnet'] = input('What is your subnet mask?\n Example: 255.255.255.0\n')
                if not re.match(r'^(255|254|252|248|240|224|192|128|0)\.(255|254|252|248|240|224|192|128|0)\.(255|254|252|248|240|224|192|128|0)\.(255|254|252|248|240|224|192|128|0)$',startConfig['subnet']):
                    raise ValueError('Invalid mask.  Try again.')
                break
            except ValueError as e: print(e)
        while True:
            startConfig['manVlan'] = input('Which VLAN will you use for management?\n Example: 42\nVlan: ')
            if int(startConfig['manVlan']) > 1 and int(startConfig['manVlan']) < 1001:
                break
            elif int(startConfig['manVlan']) == 1:
                raise ValueError('This is the default VLAN and is not recommended for management traffic.')
            else: raise ValueError('Invalid vlan ID.  Please choose a number between 2 and 1000')
        while True:
            try:
                startConfig['console'] = input('Lastly, which console port are you using?\n Examle: COM1\n').upper()
                if not re.match(r'^COM[0-5]$', startConfig['console']):
                    raise ValueError('Invalid console port, try again.')
                break
            except ValueError as e: print(e)

        # Send the data collected to a script to send the appropriate commands to the device
        serialConnect.cerealFunk(startConfig)
        # Tell the user they can now SSH to their device
        print(f"You can now SSH to {startConfig['hostname']} with the credentials you provided.")

    def show_menu(self):    # Create a menu for device_type that was selected by the user
        print('-' * 42)     # Separators for the Title
        print((f"{self.device_type} Configuration Menu").center(42))
        print('-' * 42)
        for i, option in enumerate(self.menu_options, 1):
            print(f"{i}. {option}")     # Starting at 1, prints the menu options available
        print()                         # Menu options are defined by device_type

    # This function just handles what happens when the user makes a valid selection from the menu.
    def handle_menu_choice(self, choice):
        if choice == 1:  # choice is the same for both router and switch, run start_configuration()
            self.start_configuration()
        elif choice == 2:   # We will have to create an 'if' block here to find out which device is currently selected
            print('Under construction')
        elif choice == 3:   # Same as choice 2, create an 'if' block
            print(f"You chose option 3 for {self.device_type}.")
        else:
            print("Invalid choice. Please enter a valid number.\n")

# Here we define what questions will be processed by the start_configuration method
router_questions = (['hostname', 'username', 'password', 'ipDomain', 'manInt', 'manIp', 'subnet', 'console'])
# This is an adjustable list of options for our show_menu method
router_menu = ["Initial Configuration", "OSPF", "Local AAA"]
# This defines our device object type and variables
router = Device("Router", router_questions, router_menu)

# Same logic from router for switch
switch_questions = ["hostname", "username", "password", "ipDomain", "manInt", "manIp", "subnet", "console", "manVlan"]
switch_menu = ["Initial Configuration", "Local AAA", "To-be-determined option"]
switch = Device("Switch", switch_questions, switch_menu)

# Create a dictionary to represent our first menu
devices = {"1": router, "2": switch}
#if devices == router:
#    Device.configuration_questions = router_questions
#elif devices == switch:
#    Device.configuration_questions = switch_questions
print('-' * 42)
print('Auto Configure Cisco Devices'.center(42))    # Main Program Starts Here
print('-' * 42)

exitFlag = False    # I had a loop error and creating this exitFlag fixed it... Don't touch it for now

while not exitFlag: # Basically a while True loop
    # Prompt the user to choose a device_type
    answer = input("1. Router\n2. Switch\nPlease select a device to configure: ")
    
    device = devices.get(answer)    # Get the device type from the dictionary
    
    if device:      # device must have a value
        device.show_menu()  # show the menu for the selected device
        
        while True:     # Prompt the user to make a choice from the menu
            choice = input(f"Please select an option for {device.device_type} (1-{len(device.menu_options)}): ")
            try:
                choice = int(choice)    # Convert the choice to an int and pass thru to the menu handler
                device.handle_menu_choice(choice)
            except ValueError:  # If the user input something not in the list, reprompt them
                print("Invalid choice. Please enter a valid number.\n")
                continue
    exitFlag = True     # Exit the loop to continue with device questions or whatever the menu handler does       
