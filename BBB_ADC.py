import sys
import subprocess 
import string


acceptableInputPins = { 'P9-39':'AIN0', 'P9-40':'AIN1', 'P9-37':'AIN2', 'P9-38':'AIN3', 'P9-33':'AIN4', 'P9-36':'AIN5', 'P9-35':'AIN6' }

def Initialize():
	findSlotsLocation = """sudo find /sys/devices/bone_capemgr.*/ -name "slots" """
	process = subprocess.Popen( findSlotsLocation, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )	
	slotsLocation = process.communicate()[0].rstrip()
	if process.returncode != 0:
		print "Could not find the path to .../bone_capemgr.*/slots"	
	else:
		turnOnAdc = """sudo sh -c "echo 'BB-ADC' > """ +  slotsLocation + """" """ 
		process = subprocess.Popen( turnOnAdc, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )	
		process.communicate()
		if process.returncode != 1:
			print "ADC ports could not be enabled"	
		else:
			print "ADC ports enabled"
	
def GetValueRaw( inputPin ):	  
	if inputPin in acceptableInputPins:
		pinName = acceptableInputPins[inputPin]
	elif inputPin in acceptableInputPins.values():
		pinName = inputPin 
	pinNumber = pinName[len(pinName)-1]

	searchName = '*in_voltage' + pinNumber + '_raw'
	searchCommand = 'sudo find /sys/ -name ' + searchName  # the shell command
	process = subprocess.Popen(searchCommand, stdout=subprocess.PIPE, stderr=None, shell=True)
	adcValueLocation = process.communicate()[0].rstrip()

	getValueCommand = 'cat ' + adcValueLocation
	process = subprocess.Popen(getValueCommand, stdout=subprocess.PIPE, stderr=None, shell=True)
	process = subprocess.Popen(getValueCommand, stdout=subprocess.PIPE, stderr=None, shell=True) # get value twice b/c of bug in ADC driver
	adcValue = process.communicate()[0].rstrip()
	
	return int(adcValue)


def GetValueScaled( inputPin ):
	return float(GetValueRaw(inputPin))/4096


def GetValueMillivolts(inputPin):
	return GetValueScaled(inputPin)*1800
	
		
