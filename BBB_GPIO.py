# BBB_GPIO
import sys
import subprocess 
import string

def RunCommand( command ):
	process = subprocess.Popen( command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True )	
	response = process.communicate()
	returnDict = { 'returncode': process.returncode, 'output':response[0].rstrip(), 'error': response[1].rstrip() }
	return returnDict

class GPIO_PIN_BASE:
  
  def __init__(self,pinNum,direction):
    if direction not in ['in', 'In', 'IN', 'out', 'Out', 'OUT']:
      raise ValueError("""direction must be 'in' or 'out'""")
    self.pinNum = pinNum 
    if direction in ['in', 'In', 'IN']:
      self.direction = 'in'
    else:
      self.direction = 'out'
    initialize = self.InitializeGpioPin()
    if not (initialize['returncode'] == 0 or ( initialize['returncode'] == 1 and initialize['error'] == "")):
    	raise Exception("Didn't initialize properly")
    else:
    	print "initialized properly"
    	setDirection = self.SetDirection(pinNum, direction)
    	if setDirection['returncode'] != 0 :
    		raise Exception("Didn't set direction properly")
    	else:
   		print "set direction properly"
    		#if self.direction == 'out':  
      
  def InitializeGpioPin(self):
    command = """sudo sh -c "echo '""" + str(self.pinNum) + """' > /sys/class/gpio/export" """ 
    print command
    return RunCommand( command )
   
   
  def SetDirection(self, pinNum, direction):
    if direction == 'out':
    	command = """sudo sh -c "echo 'low' > /sys/class/gpio/gpio""" + str(pinNum) + """/direction" """ 
    else:
    	command = """sudo sh -c "echo 'in' > /sys/class/gpio/gpio""" + str(pinNum) + """/direction" """
    return RunCommand( command )

	
 
