import sys
import subprocess 
import string


acceptablePwmPins = ['P8_13']
# 'P9_14', 'P9_16' partially work
# 'P8_19'  doesnt work

availableOperations = ['run', 'duty', 'period', 'frequency', 'polarity']

def RunCommand( command ):
	process = subprocess.Popen( command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )	
	response = process.communicate()
	returnDict = { 'returncode': process.returncode, 'output':response[0].rstrip(), 'error': response[1].rstrip() }
	return returnDict

def GetHzFromNanoSeconds( nanoSeconds ):
	frequency = float( 1000000000 / nanoSeconds )
	return int(frequency)

def GetNanoSecondsFromHz( hz ):
	period = float( 1000000000 / hz )
	return int(period)

def InitializePin( outputPin, period=None, duty=None, polarity=None ):
	if outputPin not in acceptablePwmPins:
		print outputPin + ' is an invalid pwm pin. Acceptable pins are ' + ', '.join(acceptablePwmPins)
	else:	
		findSlotsLocation = RunCommand( """sudo find /sys/devices/bone_capemgr.*/ -name "slots" """ )
		if findSlotsLocation['returncode'] != 0:
			print "Could not find the path to .../bone_capemgr.*/slots"	
		else:
			turnOnPwmCommand = """sudo sh -c "echo 'am33xx_pwm' > """ + findSlotsLocation['output'] + """" """ 
			turnOnPwm = RunCommand( turnOnPwmCommand )
			if turnOnPwm['returncode'] != 0:
				print "PWM ports could not be enabled.  " + turnOnPwmCommand + " command failed." 
			else:				
				setupOutputPinCommand = """sudo sh -c "echo 'bone_pwm_""" + outputPin + """' > """ +  findSlotsLocation['output'] + """" """ 
				setupOutputPin = RunCommand( setupOutputPinCommand )
				if setupOutputPin['returncode'] != 1:
					print "Pin " + outputpin + " could not be enabled. " + setupOutputPinCommand + " command failed."
				else:
					SetRun( outputPin, 0)
					if period is None:
						SetPeriod(outputPin, 500000)
					else:
						SetPeriod(outputPin, period)
					if duty is None:
						SetDuty(outputPin, 0)
					else:
						SetDuty(outputPin, duty)
					if polarity is None:
						SetPolarity(outputPin, 0)
					else:
						SetPolarity(outputPin, polarity)
					SetRun( outputPin, 1)				
								
					print "PWM driver and pin " + outputPin + " enabled"
					return 0
	return -1
	

					
def SetValue( outputPin, operation, value ):
	if outputPin not in acceptablePwmPins:
		print outputPin + ' is an invalid pwm pin. Acceptable pins are ' + ', '.join(acceptablePwmPins)
	else:
		findOperationCmd = """find /sys/devices/ocp.3/pwm_test_""" + outputPin + """.*/""" + operation
        	findOperation = RunCommand( findOperationCmd )
 		if findOperation['returncode'] != 0:
                	print 'Command: ' + findOperationCmd + ' failed'
        	else:				
			operationCommand = """sudo sh -c "echo '""" + str(int(value)) + """' > """ + findOperation['output'] + """" """
			operationResponse = RunCommand( operationCommand )
			if operationResponse['returncode'] != 0:
				print 'Command: ' + operationCommand + ' failed'
			else:				
				print operation + ' set to ' + str(value)
				return 0
	return -1
		
	
def SetRun( outputPin, value ):	  
	return SetValue( outputPin, 'run', value)
			
def SetPeriod( outputPin, value ):
        return SetValue( outputPin, 'period', value)

def SetFrequency( outputPin, value ):
	periodValue = GetNanoSecondsFromHz( value )
        return SetValue( outputPin, 'period', periodValue )

def SetDuty( outputPin, value ):
        return SetValue( outputPin, 'duty', value)

def SetPolarity( outputPin, value ):
	return SetValue( outputPin, 'polarity', value)


def GetValue( outputPin, operation ):
	if outputPin not in acceptablePwmPins:
                print outputPin + ' is an invalid pwm pin. Acceptable pins are ' + ', '.join(acceptablePwmPins)
        else:
		if operation not in availableOperations:
			print 'can only get values for ' + ', '.join(availableOperations)
		else:
			findOperationCmd = """find /sys/devices/ocp.3/pwm_test_""" + outputPin + """.*/""" + operation
	                findOperation = RunCommand( findOperationCmd )
	       		if findOperation['returncode'] != 0:
	                	print 'Command: ' + findOperationCmd + ' failed' 
	            	else:
				operationValueCommand = """sudo cat """ + findOperation['output']
				operationValue = RunCommand( operationValueCommand )
	                      	if operationValue['returncode'] != 0:
	                        	print 'Command: ' + operationValueCommand + ' failed'
	                	else:
	                        	return int( operationValue['output'] )
	return -1

		
def GetRun( outputPin ):	  
	return GetValue( outputPin, 'run')

def GetPeriod( outputPin ):
	return GetValue( outputPin, 'period')

def GetFrequency( outputPin ):
	return GetHzFromNanoSeconds( GetPeriod( outputPin) )

def GetDuty( outputPin ):
	return GetValue( outputPin, 'duty' )

def GetPolarity( outputPin ):
	return GetValue( outputPin, 'polarity')
