import random

def check_valid_input(letter_guessed, old_letters_guessed ):
     if letter_guessed in old_letters_guessed:
         return False
     
     if len(letter_guessed)==1 and  letter_guessed.isalpha():
        return True
     else:
        return False
     
    
   


# סעיף 1: הדפסת הודעת פתיחה
print("Welcome to the game Hangman.")
MAX_TRIES =6
# סעיף 2: הדפסת ASCII Art בעזרת מרכאות משולשות ו-backslash
HANGMAN_ASCII_ART =r"""\
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/                    

+---+
   |   |
   O   |
  /|\  |
  / \  |
       |
========= 

      ______
   .-'      '-.
  /            \
 |              |
 |,  .-.  .-.  ,|
 | )(_o/  \o_)( |
 |/     /\     \|
 (_     ^^     _)
  \__|IIIIII|__/
   | \IIIIII/ |
   \          /
    `--------`   
"""
print(HANGMAN_ASCII_ART)

# סעיף 3: הדפסת מספר אקראי בין 5 ל-10
print(random.randint(5, 10))

# סעיף 4: רשימת המצבים של האיש התלוי
HANGMAN_PICS = [
    r"""\
    x-------x
    """,
    r"""\
    x-------x
    |
    |
    |
    |
    |
    """,
    r"""\
    x-------x
    |       |
    |       0
    |
    |
    |
    """,
    r"""\
    x-------x
    |       |
    |       0
    |       |
    |
    |
    """,
    r"""\
    x-------x
    |       |
    |       0
    |      /|\
    |
    |
    """,
    r"""\
    x-------x
    |       |
    |       0
    |      /|\
    |      /
    |
    """,
    r"""\
    x-------x
    |       |
    |       0
    |      /|\
    |      / \
    |
    """
]

# הדפסת כל מצבי האיש התלוי the arr i made
#for i, pic in enumerate(HANGMAN_PICS):
#    print(f"Picture {i + 1}:")
 #   print(pic)
old_letters_guessed =[]
word_to_guess=input("enter a word that pepole will guess")
encrypted_word_to_guess= " _"* (len(word_to_guess))
print(encrypted_word_to_guess)

second_list = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]


guess=input("guess a letters")
print(check_valid_input(guess,old_letters_guessed))
old_letters_guessed.append(guess)

while guess != '*':
    guess=input("guess a letters")
    print(check_valid_input(guess,old_letters_guessed))
    old_letters_guessed.append(guess)





