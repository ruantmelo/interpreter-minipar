import os


from interfaces.interface_parser import IParser
from interfaces.interface_execute import ExecutorInterface
from interfaces.interface_logger import ILogger
class Interpreter:
  def __init__(self, logger=ILogger, Parser=IParser, Executor=ExecutorInterface):
    self._parser = Parser(logger=logger)
    self._executor = Executor(logger=logger)

  def run(self, program):
    parse_tree = self._parser.parsing(program)

    self._executor.reset()
    self._executor.execute(parse_tree)
  

if __name__ == '__main__':
  source = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'test5-server.mp')
  
  with open(source, 'r') as file:
    source = file.read()
    interpreter = Interpreter(source)
    interpreter.run()
  