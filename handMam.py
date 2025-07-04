import random

def check_valid_input(letter_guessed, old_letters_guessed ):
  if letter_guessed in old_letters_guessed:
      return False
  
  
  if len(letter_guessed)==1 and  letter_guessed.isalpha():
    return True
  else:
    return False
     
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
  if check_valid_input(letter_guessed,old_letters_guessed):
    old_letters_guessed.append(guess)
    return True
  else:
    return "X\n" + " -> ".join(sorted(old_letters_guessed))
  
def show_hidden_word(secret_word, old_letters_guessed):
  #encrypted_word_to_guess= " _"* (len(word_to_guess))
  encrypted_word_to_guess=""
  for item in secret_word:
    if item in old_letters_guessed:
      encrypted_word_to_guess+=item
    elif item == ' ':
      encrypted_word_to_guess+=' '
    else:
      encrypted_word_to_guess+='_'
    encrypted_word_to_guess+=' '
  return encrypted_word_to_guess


def check_win(secret_word, old_letters_guessed):
  for item in secret_word:
    if not item in old_letters_guessed:
      return False
  return True


   


  

  


     
         
         
     
     
    
   


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
#encrypted_word_to_guess= " _"* (len(word_to_guess))
print(show_hidden_word(word_to_guess,old_letters_guessed))

second_list = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
num_of_guess=0
#letter_guessed=[]
guess =''
while num_of_guess != 7 or check_win(word_to_guess,old_letters_guessed):
    guess=input("guess a letters")
    if(check_valid_input(guess,old_letters_guessed)):
      try_update_letter_guessed(guess,old_letters_guessed) 
    if not guess in word_to_guess:
      print(HANGMAN_PICS[num_of_guess])
      num_of_guess+=1
      

#print(old_letters_guessed)
print(show_hidden_word(word_to_guess,old_letters_guessed))
print(check_win(word_to_guess,old_letters_guessed))




