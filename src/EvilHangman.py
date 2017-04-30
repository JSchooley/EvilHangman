'''
Created on Sep 23, 2016

Josh Schooley
'''
'''
EvilHangman.py
'''

import sys
import random

class EvilHangman:
    '''
    Initializes the words list
    '''
    def __init__(self):
        file = open(sys.argv[1],'r')

        self.words = []

        self.wordguess = []

        for line in file:
            self.words.append(line.rstrip())
        
        # This code was used for testing all of the 5 letter words in the english language
        #self.words = file.read().split()
        #print len(self.words)
    '''
    Outputs the current status of the guesses
    '''
    def printword(self):
        for c in self.wordguess:
            print c,

        print('\n\n')
        
    # Helper method to do all of the breaking apart and putting back together
    def wordFamilies(self, wordList, guessedLetter):
        # Variable to hold the best chance to make the user lose
        bestFamily = []
        wordLength = len(wordList[0])
        # Variable that sets the family keys
        currentFamily = ['_'] * wordLength
        # Dictionary with the key being the word family
        # and the values being the list of words in that family
        tempFamilies = {}
        # The list of the families
        familiesList = []
        
        # For all of the words, get the families by replacing
        # all instances of '_' to the guessed letter
        for word in wordList:
            currentFamily = ['_'] * wordLength
            for i in range(len(word)):
                if word[i] == guessedLetter:
                    currentFamily[i] = guessedLetter
            # Gets the string that is the current family being made
            currentFam = (str(currentFamily))
            # Populatesthe list of all families, excluding duplicates
            if currentFam not in familiesList:
                familiesList.append(currentFam)
            # Either adds the key to the dictionary with the word that
            # made that family or appends the word to an existing key
            if currentFam not in tempFamilies:
                tempFamilies[currentFam] = [word]
            else:
                tempFamilies[currentFam].append(word)
        # Variable that keeps track of which family list has the most words
        most = 0
        # Finds which family has the most words and sets it to bestFamily
        for j in range(len(familiesList)):
            if len(tempFamilies[familiesList[j]]) > most:
                most = len(tempFamilies[familiesList[j]])
                bestFamily = familiesList[j]
        # Index to parse bestFamily
        bestIndex = 2
        # Gets all new found letters and adds them to our word guess
        for k in range(wordLength):
            if self.wordguess[k] == "_" and bestFamily[bestIndex] != "_":
                self.wordguess[k] = guessedLetter
            bestIndex += 5
        # Returns the new list of possible words
        return tempFamilies[bestFamily]

    def playgame(self):
        wordSet = []
        
        # Gets the number of guesses from the user
        while True:
            guesses = raw_input('Enter how many guesses you want (Pick a number 0 or greater):')
            if not (guesses.isdigit()):
                print "You must enter a positive integer"
            else:
                guesses = int(guesses)
                if guesses > 0:
                    break
                else:
                    print "The number of guesses needs to be 3 or more"
            
        # Gets the size of the word from the user
        while True:
            wordLen = raw_input('Enter the length of the word you want to guess (Pick a number 3 or greater):')
            if not (wordLen.isdigit()):
                print "You must enter a positive integer"
            else:
                wordLen = int(wordLen)
                if wordLen < 3:
                    print "The size of the word needs to be longer than 2 letters"
                else:
                    self.wordguess = ['_'] * wordLen
                    for word in self.words:
                        if len(word) == wordLen:
                            wordSet.append(word)
                    if len(wordSet) == 0:
                        print "There are no words in our dictionary of that length. Please enter another length"
                    else:
                        print wordSet
                        break
            
        # List of letters that have been guessed
        guessed = []
        
        self.printword()
        # While the user hasn't guessed the amount of times specified
        while guesses != 0:
            # Get the input from the user and convert to lower case
            ch = raw_input('Enter a guess:').lower()
            # Int that checks for the win condition
            win = 0
                
            # If the input isn't a letter...
            if not ch.isalpha():
                print "I only accept letters of the alphabet"
            # If the input has already been guessed...
            elif ch in guessed:
                print "You've already guessed that letter! Try another"
            # If the input is more than one letter...
            elif len(ch) > 1:
                print "I need a single letter, please"
            # If the input is just the return...
            elif len(ch) == 0:
                print "I need at least one letter"
            else :
                # Add the guess to the guessed list
                guessed.append(ch)
                # Calls helper to find the best set of words to cheat with
                wordSet = self.wordFamilies(wordSet, ch)
                
                print "List of remaining words:", wordSet
                
                # Checks if they have won
                for letter in self.wordguess:
                    if letter == "_":
                        win = win + 1
                
                # Winning message
                self.printword()
                if win == 0:
                    print "Congratulations, you win!"
                    break
                    
                guesses -= 1
                print "You have", guesses, "guesses remaining"
        
        # Losing message
        if win != 0:
            print wordSet[random.randint(0, len(wordSet)-1)], "was the word, sorry! Better luck next time!"
        

if __name__ == "__main__":
    print len(sys.argv)
    if len(sys.argv) != 2:
        print 'Usage: python Hangman <wordfile>'
        quit()

    game = EvilHangman()

    game.playgame()