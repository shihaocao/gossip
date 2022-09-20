from unittest import result
from src.state import State, DataPoint
import time

def test_update_node():
  test_state = State('111', 222)
  
  now = int(time.time()) - 100
  test_state.update_node('123', 456, now, 1)
  assert {'123': {456: DataPoint(now, 1)}} == dict(test_state.ip_map)

  # test override
  now += 1
  test_state.update_node('123', 456, now, 2)
  assert {'123': {456: DataPoint(now, 2)}} == dict(test_state.ip_map)
  
  # test adding rest to dictionary
  test_state.update_node('123', 457, now+1, 3)
  assert {'123': {456: DataPoint(now, 2), 457: DataPoint(now+1, 3)}} == dict(test_state.ip_map)
  test_state.update_node('123', 458, now+2, 4)
  assert {'123': {456: DataPoint(now, 2), 457: DataPoint(now+1, 3), 458: DataPoint(now+2, 4)}} == dict(test_state.ip_map)
  
  # test only keeping the three newest ports
  test_state.update_node('123', 459, now+3, 5)
  assert {'123': {459: DataPoint(now+3, 5), 457: DataPoint(now+1, 3), 458: DataPoint(now+2, 4)}} == dict(test_state.ip_map)
  
  # reject old updates
  test_state.update_node('123', 458, now-200, 9)
  assert {'123': {459: DataPoint(now+3, 5), 457: DataPoint(now+1, 3), 458: DataPoint(now+2, 4)}} == dict(test_state.ip_map)

  # reject future updates
  test_state.update_node('123', 458, now+200, 9)
  assert {'123': {459: DataPoint(now+3, 5), 457: DataPoint(now+1, 3), 458: DataPoint(now+2, 4)}} == dict(test_state.ip_map)

  # expecting add to banned set, causes state to be removed
  test_state.add_to_banned_set('123', 459)
  assert {'123': {457: DataPoint(now+1, 3), 458: DataPoint(now+2, 4)}} == dict(test_state.ip_map)
  assert ('123', 459) in test_state.banned_set

  # test reject update into banned set
  test_state.update_node('123', 459, now+3, 5)
  assert {'123': {457: DataPoint(now+1, 3), 458: DataPoint(now+2, 4)}} == dict(test_state.ip_map)

  # test multi ip membership
  test_state.update_node('123.10', 42, now, 1)
  assert {'123.10': {42: DataPoint(now, 1)}, '123': {457: DataPoint(now+1, 3), 458: DataPoint(now+2, 4)}} == dict(test_state.ip_map)

  
def test_get_state():
  test_state = State('111', 222)
  
  now = int(time.time()) - 100
  test_state.update_node('123', 456, now, 1)
  test_state.update_node('123', 457, now, 2)
  test_state.update_node('123', 458, now, 3)
  test_state.update_node('123.10', 1, now, 4)
  test_state.update_node('123.10', 2, now, 5)
  test_state.update_node('123.10', 3, now, 6)

  result_list = test_state.get_state()
  expected_list = [f'123:456,{now},1',
                   f'123:457,{now},2',
                   f'123:458,{now},3',
                   f'123.10:1,{now},4',
                   f'123.10:2,{now},5',
                   f'123.10:3,{now},6',
                   f'111:222,0,0'
                   ]

  assert expected_list == result_list
  test_state.update_self(now+1, 5)
  result_list = test_state.get_state()
  expected_list = [f'123:456,{now},1',
                   f'123:457,{now},2',
                   f'123:458,{now},3',
                   f'123.10:1,{now},4',
                   f'123.10:2,{now},5',
                   f'123.10:3,{now},6',
                   f'111:222,{now+1},5'
                   ]

  assert expected_list == result_list

def test_get_random_ip():
  test_state = State('111', 222)
  
  now = int(time.time()) - 100
  test_state.update_node('123', 456, now, 1)
  test_state.update_node('123', 457, now, 2)
  test_state.update_node('123', 458, now, 3)
  test_state.update_node('123.10', 1, now, 4)
  test_state.update_node('123.10', 2, now, 5)
  test_state.update_node('123.10', 3, now, 6)
  
  ip, port = test_state.get_random_ip()
  print(ip)
  print(port)
  