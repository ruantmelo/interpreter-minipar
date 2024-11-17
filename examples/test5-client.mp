SEQ
  chan calculadora("localhost", "localhost")
  int resultado
  calculadora.send("+", 5, 4)
  calculadora.receive(resultado)

  output(resultado)

