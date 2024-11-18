PAR
    # Fatorial
    int n
    n = 20

    int value
    value = 1

    int i
    i = 1

    while(i <= n) {
        value = value * i
        i = i + 1
        output("increment FATORIAL")
    }

    output(value)

PAR
    # Fibonacci
    int n2
    n2 = 10

    int j
    j = 2

    int prev
    prev = 1
    
    int curr
    curr = 1

    int temp
    
    while (j < n2)
    {
        temp = curr
        curr = prev + curr
        prev = temp
        j = j + 1

        output("increment FIBONACCI")
    }

    output(curr)