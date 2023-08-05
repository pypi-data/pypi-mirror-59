# MicroBitTools
MicroBitTools is a package for making BBC MicroBit development easier.

# Installation
Run the following line in the terminal/command prompt to install:

```pip install MicroBitTools```


# Examples
This one is used to flash to the MicroBit
```
from MicroBitTools import flash
flash("PythonFilePathHere", "MicroBitDirectoryHere")
```


This one is used to flash whole folders
```
from MicroBitTools import flashF
flashF("PythonFilePathHere", "MicroBitDirectoryHere")
```


# Serial system (Still in early development)
First, let's create a SerialSystem
```
import MicroBitTools as mbt
mbs = mbt.SerialSystem()
```
Then, let's move the SerialSystem on to the MicroBit
```
mbs.readyMicroBit()
```
After that, we are going to create a loop that is printing the data from the MicroBit
```
while True:
    print(mbs.read())
```
You'r code should look like this:
```
import MicroBitTools as mbt
mbs = mbt.SerialSystem()

mbs.readyMicroBit() # Load 

while True: # Infinite loop
    print(mbs.read()) # Print data from MicroBit
```