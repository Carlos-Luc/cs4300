def sign_check(num):

    if(num > 0):

        return "positive"
    
    elif(num < 0):

        return "negative"
    
    else:

        return "zero"

def first_ten_primes():

    ten_primes = []

    for i in range(2,101):

        is_prime = True

        for j in range (2,i):

            if(i % j == 0):

                is_prime = False

                break

        if is_prime:

            ten_primes.append(i)
        
        if len(ten_primes) == 10:

            break
    
    for num in ten_primes:

        print(num)

        

def sum_one_to_hundered():

    sum = 0

    i = 1

    while i <= 100:

        sum += i

        i += 1
    
    return sum
