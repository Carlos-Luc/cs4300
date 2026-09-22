def calculate_discount(price,discount):

    if(price < 0):

        raise ValueError("Price cannot be less than zero")
    
    if(discount < 0 or discount > 100):

        raise ValueError("Discount cannot be less than zero or more than 100")

    result = price - (price * (discount/100))

    return round(result,2)