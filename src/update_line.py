class IP:
  ip: str = None
  def __init__(self, ip_str: str):
    MAX_IP_LEN = 64
    if len(ip_str) > MAX_IP_LEN:
      # too long
      return
    
    subnets = ip_str.split('.')
    if len(subnets) != 4:
      # incorrect subnets
      return
    
    try:
      subnets_as_ints = [int(x) for x in subnets]
      if min(subnets_as_ints) < 0:
        return
      if max(subnets_as_ints) > 255:
        return
    except:
      return
    
    # must be a valid ip now
    self.ip = ip_str

class Port:
  port: int = None
  def __init__(self, port_as_str: str):
    try:
      data = int(port_as_str)
      if 0 <= data < 9999:
        self.port = data
    except:
      pass

class Digit:
  digit: int = None
  def __init__(self, digit_as_str: str):
    try:
      data = int(digit_as_str)
      if 0 <= data < 10:
        self.digit = data
    except:
      pass
      
class UpdateTime:
  update_time: int = None
  def __init__(self, update_time: str):
    try:
      data = int(update_time)
      if 0 <= data:
        self.update_time = data
    except:
      pass

class UpdateLine:
  valid: bool      = False
  ip: str     = None
  port: int   = None
  update_time: int = None
  digit: int       = None
  
  def __init__(self, update_line: str):
    MAX_LINE_LEN = 1000
    if len(update_line) > MAX_LINE_LEN:
      return
    
    split_on_commas = update_line.split(',')
    if len(split_on_commas) != 3:
      return
    
    ip_port_str = split_on_commas[0]
    ip_port_list = ip_port_str.split(':')
    if len(ip_port_list) != 2:
      return
    
    ip_str, port_str = ip_port_list
    ip = IP(ip_str)
    port = Port(port_str)
    update_time = UpdateTime(split_on_commas[1])
    digit = Digit(split_on_commas[2])
    
    self.ip = ip.ip
    self.port = port.port
    self.update_time = update_time.update_time
    self.digit = digit.digit
    
    # print(f'{ip.ip}, {port.port}, {update_time.update_time}, {digit.digit}')
    
    if (    ip.ip is not None
        and port.port is not None
        and update_time.update_time is not None
        and digit.digit is not None):
      self.valid = True