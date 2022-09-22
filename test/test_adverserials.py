from src.adversarial import *

class TestFixture:
  def __init__(self):
    self.state = State('111', 222)

    now = int(time.time()) - 100
    self.state.update_node('123', 456, now, 1)
    self.state.update_node('123', 457, now, 2)
    self.state.update_node('123', 458, now, 3)
    self.state.update_node('123.10', 1, now, 4)
    self.state.update_node('123.10', 2, now, 5)
    self.state.update_node('123.10', 3, now, 6)


def test_attacks():
  tf = TestFixture()
  print(random_data(tf.state, '1.1.1.1', 3000))
  print(negative_digits(tf.state, '1.1.1.1', 3000))
  print(long_response(tf.state, '1.1.1.1', 3000)[:1000])
  print(change_their_digit(tf.state, '1.1.1.1', 3000))
  print(whitespace_in_state(tf.state, '1.1.1.1', 3000))
  print(bad_ip_port(tf.state, '1.1.1.1', 3000))
