import os

from parser import Parser
from executor import Executor

class Interpreter:
  def __init__(self, program):
    self.program = program
    self.parser = Parser()
    self.executor = Executor()

  def run(self):
    parse_tree = self.parser.parsing(self.program)
    print(parse_tree)
    self.executor.execute(parse_tree)
  

if __name__ == '__main__':
  source = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'test5-client.mp')

  print("Source: ", source)
  with open(source, 'r') as file:
    source = file.read()
    interpreter = Interpreter(source)
    interpreter.run()
  