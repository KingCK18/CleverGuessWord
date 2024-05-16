"""
Created on 11/20/23
@author: christiankirby
"""


import random

def handleUserInputDifficulty():
    '''
    This function asks the user if they would like
    to play the game in (h)ard or (e)asy mode,
    then returns the corresponding number of misses
    allowed for the game.
    '''
    print("How many misses do you want? Hard has 8 and Easy has 12.")
    userinput = input("(h)ard or (e)asy> ").lower()
    if userinput == "h":
        return 8
    elif userinput == "e":
        return 12

def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''
    print(displayString)

    while True:
        userinput = input("letter> ").strip().lower()
        if userinput not in lettersGuesed:
            return userinput
        else:
            print("guess again, you've already guessed that")

# New Functions

def handleUserInputDebugMode():
    '''
    This function will prompt the user if they wish to play in debug mode.
    True is returned if the user enters the letter “d”, indicating debug mode was chosen;
    False is returned otherwise.
    '''
    userinput = input("Which mode do you want: (d)ebug or (p)lay: ").lower()
    return userinput == "d"

def handleUserInputWordLength():
    '''
    The length of secretWord is no longer randomized,
    instead, the user will be asked how long secretWord should be.
    You do not need to check for bad user input.
    '''
    userinput = int(input("How many letters in the word you'll guess: "))
    return userinput

def createTemplate(currTemplate, letterGuess, word):
    '''
    This function will create a new template for the secret word that the user will see.
    This new template should be consistent with the currentTemplate and word.
    '''
    new_template = ''
    for ct, w in zip(currTemplate, word):
        if ct == '_' and w == letterGuess:
            new_template += letterGuess
        else:
            new_template += ct
    return new_template

def getNewWordList(currTemplate, letterGuess, wordList, debug):
    '''
    This function constructs a dictionary of strings as the key to lists as the value.
    It does this by calling createTemplate on every word in wordList with currTemplate and letterGuess.
    The string createTemplate returns is a key into the dictionary and the current word from wordList is added to the list that maps to that key.
    '''
    template_dict = {}

    for word in wordList:
        key = createTemplate(currTemplate, letterGuess, word)
        if key not in template_dict:
            template_dict[key] = [word]
        else:
            template_dict[key].append(word)

    if debug:
        print("\n".join(sorted(f"{key} : {len(value)}" for key, value in template_dict.items())))
        print(f"# keys = {len(template_dict)}")

    max_key = max(template_dict, key=lambda k: (len(template_dict[k]), k.count('_')))
    return max_key, template_dict[max_key]

def processUserGuessClever(guessedLetter, guessedWordAsList, missesLeft):
    '''
    Takes the user's guess, the user's current progress on the word,
    and the number of misses left; updates the number of misses left
    and indicates whether the user missed.
    '''
    if guessedLetter in guessedWordAsList:
        missesLeft += 1
    else:
        missesLeft -= 1
    return missesLeft

def createDisplayString(lettersGuessed, missesLeft, guessedWordAsList):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    letters_Guessed = set(sorted(lettersGuessed))
    # Remove guessed letters from alphabet
    for letter in range(len(alphabet)):
        for i in letterGuessed:
            if i == alphabet[letter]:
                alphabet[letter] = " "
            #alphabet.remove(letter)

    not_guessed_str = "".join(alphabet)
    guessed_word_str = "".join(str(letter) if letter in letters_Guessed else "_" for letter in guessedWordAsList)

    display_string = f"letters not yet guessed: {not_guessed_str}\nmisses remaining = {missesLeft}\n{guessed_word_str}"
    return display_string

def runGame(filename):
  f = open(filename)
  data = [line.strip() for line in f]
  f.close()
  wins = 0
  losses = 0

  debug = handleUserInputDebugMode()
  misses_allowed = handleUserInputDifficulty()
  secret_word_length = handleUserInputWordLength()

  # Check if there are words of the specified length in the data
  valid_words = [word for word in data if len(word) == secret_word_length]
  if not valid_words:
    print(f"No words of length {secret_word_length} found.")
    return False

  secret_word = random.choice(valid_words)
  guessed_word_as_list = ['_' for _ in range(secret_word_length)]
  lettersGuessed = []
  misses_left = misses_allowed

  while "_" in guessed_word_as_list and misses_allowed > 0:
     display_string = createDisplayString(lettersGuessed, misses_left,
                                          guessed_word_as_list)
     guessed_letter = handleUserInputLetterGuess(lettersGuessed, display_string)
     lettersGuessed.append(guessed_letter)
     guessed_letter = guessed_letter[0]

    # Update guessed word and data
     curr_template, data = getNewWordList("".join(guessed_word_as_list), guessed_letter, data, debug)
     secret_word = random.choice([word for word in data if len(word) == secret_word_length])

     result = processUserGuessClever(guessed_letter, curr_template, misses_allowed)
     misses_allowed, correct_guess = result

     if not correct_guess:
      misses_left -= 1

  if debug:
     print(f"Word Is: {secret_word}")
     print(f"Guessed Word: {''.join(guessed_word_as_list)}")
     print(f"Letters Guessed: {lettersGuessed}")
     print(f"Misses Left: {misses_left}\n")

  if "_" not in guessed_word_as_list:
      print("You guessed the word:", secret_word)
      wins += 1
  elif misses_allowed <= 0:
     print("You're hung!!\nThe secret word is:", secret_word)
     losses += 1
     print("You made:", len(lettersGuessed), "guesses with:", misses_allowed, "misses")

  print("Session summary: Wins =", wins, "Losses =", losses)
  return wins > losses


if __name__ == '__main__':
  runGame('lowerwords.txt')