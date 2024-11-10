from os import listdir
from src.parser import Parser

if __name__ == '__main__':
  examples_folder = 's'

  files = listdir(examples_folder)[:1]

  for filename in files:
    with open(f'{examples_folder}/{filename}', 'r') as file:
      program = file.read()
      parser = Parser()
      result = parser.parsing(program)
      print(result)
      with open(f'{examples_folder}/{filename + ".result"}', 'w') as file:
        file.write(str(result))
      

  