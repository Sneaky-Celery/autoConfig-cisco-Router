# Scott Proctor CNA 256
import serial
import time

def cerealFunk(x):
    # Connect to the router via serial
    ser = serial.Serial(port=x['console'], baudrate=9600, timeout=1)

    # Wait for the router to be ready
    time.sleep(1)
    ser.read(ser.inWaiting())

    # Log in to the router
    ser.write(b'\r\n')
    ser.write(b'enable\r\n')
    ser.write(b'configure terminal\r\n')
    
    # Run commands pertinent to setting up SSH
    ser.write(b'hostname ' + x['hostname'] + '\r\n')
    ser.write(b'username ' + x['username'] + ' password ' + x['password'] + '\r\n')
    ser.write(b'ip domain name ' + x['ipDomain'] + '\r\n')
    ser.write(b'crypto key generate rsa\r\n')
    ser.write(b'crypto key generate rsa modulus 2048\r\n')
    ser.write(b'ip ssh version 2\r\n')
    ser.write(b'line vty 0 4\r\n')
    ser.write(b'transport input ssh\r\n')
    ser.write(b'no shutdown\r\n')
    ser.write(b'exit')
    ser.write(b'interface ' + x['manInt'] + '\r\n')
    ser.write(b'ip address ' + x['manIp'] + x['subnet'] + '\r\n')
    ser.write(b'no shutdown\r\n')

    # Save the configuration
    ser.write(b'end\r\n')
    ser.write(b'copy run start\r\n')

    # Close the serial connection
    ser.close()