
# Omega Smartsensor Python SDK    
 This Python SDK allows you to communicate with Omega Smart Sensor devices via I2C interface or Modbus interface and easily integrate them to embedded platform such as Raspberry Pi, etc...    
    
## Requirements    
 Python 3.5+    
    
## Installation & Usage
 ### PC Install    

 #### pip install    
 When installing python, ensure the option to add python to PATH is checked.
 If python is not part of the PATH, in command prompt change directory to the location of python.exe.
 Execute the pip install command.     
    
`python -m pip install omegasensor `    
   
 #### Setuptools    
 Another method to install omegasensor. Clone from repository. And Install via Setuptools from source directory:    
 
`python setup.py install --user`   
 ### Raspberry Pi Install
 #### Setuptools    
 Clone from repository. And Install via Setuptools from source directory:    
 
`python3 setup.py install --user`       
  
 ## Getting started    
      
    import time
    from omegasensor import *  
    
    def main():    
        bus = BusModbus('/dev/ttyUSB0', SMARTSENSOR_MODBUS_ADDR)   # for Modbus interface 
        # bus = BusI2C(1, SMARTSENSOR_I2C_ADDR) # for I2C interface
        ss = Smartsensor(bus)    
        
        ss.soft_reset()    
        ss.preset_config()    
        print("Firmware 0x%08x" % ss.read(R.FIRMARE_VERSION))    
        print("Device Id 0x%08x" % ss.read(R.DEVICE_ID))    
        print("Device %s" % ss.read(R.DEVICE_NAME))    
        sensor_cnt = ss.read(R.NUMBER_OF_SENSORS)    
        print("Onboard %d sensors" % sensor_cnt)    
        print("Onboard %d outputs" % ss.read(R.NUMBER_OF_OUTPUTS))    
        
        sensor_units = [ss.sensor_unit(i) for i in range(sensor_cnt)]    
        
        while True:    
            print("Time: ", ss.current_time_str())    
            for i in range(sensor_cnt):    
                print("%0.2f" % ss.sensor_reading(i),    
                      " %s" % sensor_units[i],    
                      "\t", end='')    
            print('\n')    
            time.sleep(1)    
        
        
    if __name__ == "__main__":    
        main()  
  
### Enable Software I2C interface:

(supports clock stretching for SmartSensor's I2C Interface)

Open config.txt
```
sudo nano /boot/config.txt
```

Add the following entry to the file
```
dtoverlay=i2c-gpio,bus=3
```

Save the file by hitting Ctrl+O. Enter. Reboot the Pi.

A new I2C interface can be found at `/dev/i2c-3`

SDA is BCM23 (header pin 16)

CLK is BCM24 (header pin 18)

Software I2C requires manual pull-up resistors of about 2.2k on SDA and CLK to Vcc. It may be possible to enable GPIO internal pull-up by the following commands:

```
# enable internal pull-up on pin BCM23
gpio -g mode 23 up
# enable internal pull-up on pin BCM24
gpio -g mode 24 up
```


## Examples    
    
 Examples can be found in SDK Example directory  
  
## Hardware Setup  
  
Omega BTH-SMP smart probes can be used with the I2C interface. On Raspberry Pi, here are the connections:

| Raspberry Pi | BTH-SMP |
|--|--|
|Pin 3 /BCM 2| SDA|
|Pin 5 /BCM 3| CLK|
|Pin 1| 3.3V|
|Pin 6| GND|
  
Alternatively, Omega Smart sensor dongle can be used which converts I2C interface to Modbus interface. On Linux system, the dongle will show up as /dev/ttyUSB0 or /dev/ttyACM0 for example.