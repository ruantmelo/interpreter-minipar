import os


from interfaces.interface_parser import IParser
from interfaces.interface_execute import ExecutorInterface
from interfaces.interface_logger import ILogger
from interfaces.interface_semantic import ISemantic
class Interpreter:
  def __init__(self, logger: ILogger, Parser: IParser, Semantic: ISemantic, Executor: ExecutorInterface):
    self._parser = Parser(logger=logger)
    self._executor = Executor(logger=logger)
    self._semantic = Semantic(logger=logger)
    self._logger = logger


  def run(self, program):
    try:
      parse_tree = self._parser.parsing(program)
      print(parse_tree)
      self._semantic.check_semantic(parse_tree)
      self._executor.reset()
      self._executor.execute(parse_tree)
    except Exception as exception:
      self._logger.log(repr(exception))
  

if __name__ == '__main__':
  source = os.path.join(os.path.dirname(__file__), '..', '..', 'examples', 'test5-server.mp')
  
  with open(source, 'r') as file:
    source = file.read()
    interpreter = Interpreter(source)
    interpreter.run()
  