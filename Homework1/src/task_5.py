def list_slice():

    book_list = [("Grapes of Wrath", "John Steinbeck"),("Red Rising", "Pierce Brown"),("The Count of Monte Cristo", "Alexander Dumas"),("Fahrenheit 451", "Ray Bradbury")]

    for book in book_list[:3]:

        print(book)

def create_student_dict():

    return {"Alice": 1, "Bob": 2, "Eve":3}