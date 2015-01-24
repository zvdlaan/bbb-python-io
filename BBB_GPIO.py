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
    self.InitializeGpioPin(pinNum)
    self.SetDirection(pinNum, direction)
    if self.direction == 'out':
    	"""self.SetOutputLow(pinNum)"""
    	""" ddd """
      
  def InitializeGpioPin(self, pinNum):
    command = """sudo sh -c "echo '""" + str(pinNum) + """' > /sys/class/gpio/export" """ 
    print command
    initialize = RunCommand( command )
    print("returncode: " + str(initialize['returncode']))
    print("output: " + initialize['output'])
    print("error: " + initialize['error'])
   
  def SetDirection(self, pinNum, direction):
    if direction == 'out':
    	command = """sudo sh -c "echo 'low' > /sys/glass/gpio/gpio""" + str(pinNum) + """/direction" """ 
    else:
    	command = """sudo sh -c "echo 'in' > /sys/glass/gpio/gpio""" + str(pinNum) + """/direction" """
    print command
    setDir = RunCommand( command )
    print("returncode: " + str(setDir['returncode']))
    print("output: " + setDir['output'])
    print("error: " + setDir['error'])
	
 
