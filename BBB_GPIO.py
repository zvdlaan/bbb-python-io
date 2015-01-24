# BBB_GPIO


def RunCommand(self, command ):
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
      
  def ExportToGpioLib(pinNum):
    command = """sudo sh -c "echo '""" + pinNum + """' > /sys/class/gpio/export" """ 
    export = RunCommand( command )
    print("returncode: " + str(export['returncode']))
    print("output: " + export['output'])
    print("error: " + export['error'])
    
