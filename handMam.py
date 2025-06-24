import random

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

word_to_guess=input("enter a word that pepole will guess")
encrypted_word_to_guess= " _"* (len(word_to_guess))
print(encrypted_word_to_guess)


guess=input("guess a letters")
if  not guess.isalpha() and len(guess)>1:
     print("no signs and more than two letters allowed") 
elif len(guess)>1:
    print("it can not be longer than 1 letter")

elif not guess.isalpha():
    print("no signs allowed")
else:
    guess=guess.lower()
    print("the guess was "+guess)


