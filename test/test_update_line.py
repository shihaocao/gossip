from src.update_line import UpdateLine

def test_invalid_update_line():
  inputs = [
    'foo',
    'bar',
    '100000',
  
    '123:1234:124',
    '123:124,1,1,1,1',
    'asdf:123,1,0,1,1',
    '1234.1.1.1,2,2',
    '123.1.1.1.1,2,2',
  ]
  
  updates = [UpdateLine(line) for line in inputs]
  
  for update in updates:
    assert update.valid == False
    
def test_simple_valid_update_line():
  input = '123.1.1.1:77,500,5'
  update_line = UpdateLine(input)
  assert update_line.valid       == True
  assert update_line.ip          == '123.1.1.1'
  assert update_line.port        == 77
  assert update_line.update_time == 500
  assert update_line.digit       == 5