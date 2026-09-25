def text_file_word_count(file_path):

    #Opens and reads entire text file then uses split to split each word into a list and len count the ammount of words in that list
    with open(file_path) as f:

        word_count = len(f.read().split())
    
    return word_count
