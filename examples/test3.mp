SEQ
    int n
    n = 10

    int i
    i = 2

    int prev
    prev = 1
    
    int curr
    curr = 1

    int temp
    while (i < n)
    {
        temp = curr
        curr = prev + curr
        prev = temp
        i = i + 1
    }

    output(curr)