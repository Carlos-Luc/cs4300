def sign_check(num):

    if(num > 0):

        return "positive"
    
    elif(num < 0):

        return "negative"
    
    else:

        return "zero"

def first_ten_primes():

    ten_primes = []

    #For loop checks for prime numbers from 2 to 100
    for i in range(2,101):

        #Assume current number is prime
        is_prime = True

        #for loop goes from 2 to i-1 and checks if any of these numbers can divide i evenly, if so then i is not a prime
        #it breaks out of the inner loop
        for j in range (2,i):

            if(i % j == 0):

                is_prime = False

                break

        #if i was prime then it is appended to the ten prime list
        if is_prime:

            ten_primes.append(i)
        
        #Stops when ten prime numbers are found
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
