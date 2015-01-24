# BBB_GPIO



class BBB_GPIO_PIN:
  
  def __init__(self,pinNum,direction):
    if direction not in ['in', 'In', 'IN', 'out', 'Out', 'OUT']:
      raise ValueError
    self.pinNum = pinNum 
    ifdirection in ['in', 'In', 'IN']:
      self.direction = 'in'
    else:
      self.direction = 'out'
