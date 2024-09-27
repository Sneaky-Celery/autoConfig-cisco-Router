# Import the required modules
#import paramiko to enable ssh connections in python
import serialConnect
#import pandas to read excel files

print('Welcome to your first cisco router auto configuration wizard.')
answer = input('Are you connected to the router via a console line? \y')

if answer.lower() == 'y' or answer == '':
    # Ask the user for some information first
    print('Great. Let us get some basic information from you to enable remote management of the router.\n Input the following:')
    startConfigDict = dict()
    #start working on a function to handle exceptions and invalid inputs and loop back to reprompt the user
    startConfigDict['hostname'] = input('Hostname: ')
    startConfigDict['username'] = input('Username: ')
    startConfigDict['password'] = input('Password: ')
    startConfigDict['ipDomain'] = input('What domain name will you use?\n Examples: domainName.local or studentRack4.local\n')
    startConfigDict['managedInt'] = input('What interface you use to connect remotely to this device?\n Examples: G0/0/1 or Fa0/0/1\n')
    startConfigDict['managedIP'] = input("And what will it's IP address be?\n Example: 192.168.1.1\n")
    startConfigDict['subnet'] = input('What is your subnet mask?\n Example: 255.255.255.0\n')
    startConfigDict['com'] = input('Lastly, which COM port are you using to connect?\n Examle: COM1\n')
    
    # Send the data collected to a script for creating a serial connection
    serialConnect.cerealFunk(startConfigDict)
    print('You can now connect to this device with SSH through the IP address you provided.')

elif answer.lower() == 'n' or answer.lower() == 'no':
    sshConnect = ''
    print ('Can you connect to the router through SSH? \y')
    if sshConnect.lower == 'y' or sshConnect == '':
        print('some codes')
        #Connect to device with SSH
        #ssh = paramiko.SSHClient()
        #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(ip_address, username, password)
        #stdin, stdout, stderr = ssh.exec_command('show interfaces brief')
        #result = stdout.read().decode()
        #interfaces = result.strip().split('\n')[2:]
        #interface_list = [i.split()[0] for i in interfaces]
        #print(f"Number of interfaces: {len(interface_list)}")
        #ssh.close()
    else:
        print('This program only works for COM lines and SSH.')
else:
    print('This  program only works with COM lines and SSH')

answer = print('Do you want to configure advanced security and password encryption? \y')
